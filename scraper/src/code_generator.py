import os
import sys
import requests
import random
from .names_extractor import validate_names, search_names
from .utils import init_gpt, extract_filepath
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

client, prompts = init_gpt()

MODEL = "gpt-3.5-turbo"
NUM_ITERATIONS = 30


def generate_function(html_source, url, client=None):
    html_chunks = _chunk_html(html_source)
    filepath = extract_filepath(url)

    department, university = filepath.rsplit('/', 1)[-1].split('_')[:2]
    university = university.split('.')[0]

    logging.info(f"Generating name search function for {university} {department}.")

    generated_code = _generate_code(html_chunks, client)
    _save_function(generated_code, filepath)

    iteration = 0
    while iteration < NUM_ITERATIONS:
        # if os.path.exists(filepath):
        #     # names = execute_name_search_function(html_source, filepath)
        #     # names = extract_names(html_source, url)
        # else:
        names = search_names(html_source, filepath)
        try:
            # names, _, _ = extract_names(html_source, url)
            assert len(names) > 0, "The result should be a non-empty list."
            validate_function(html_source, url)
            # if not validate_names(html_source, names):
            #     logging.info("Extracted names:\n", names)
            #     raise ValueError("Validation failed: The extracted list contains non-name items.")

            logging.info(f"Successfully generated name search function.")
            # print(names)
            _save_function(generated_code, filepath)
            break
        except Exception as e:
            error_message = str(e)
            updated_code = _update_code(generated_code, error_message, html_chunks, names, client)
            generated_code = updated_code
            iteration += 1
            logging.info(f"Updated function code due to error: {error_message}")
            _save_function(updated_code, filepath)
    else:
        logging.info(f"Test failed: Could not generate a working function after {NUM_ITERATIONS} iterations.")


def validate_function(html_source: str, url: str):
    filepath = extract_filepath(url)
    if os.path.exists(filepath):
        try:
            names = search_names(html_source, filepath)
            if names is None:
                return False

            # if validate_names(html_source, names) and validate_names_with_gpt(names, client):

            return validate_names(html_source, names)
        except Exception as e:
            logging.error(f"Validation failed: {str(e)}")
            return False

def _generate_code(source_chunks: list, client) -> str:
    combined_html_chunks = "\n".join(source_chunks)
    prompt = prompts['generate_function_prompt'].format(html_chunks=combined_html_chunks)

    try:
        httpx_logger = logging.getLogger("httpx")
        httpx_logger.setLevel(logging.WARNING)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL,
        )
        function_code = response.choices[0].message.content.strip()

        return _crop_code(function_code)
    except Exception as e:
        logging.error(f"Error while making request to OpenAI API: {str(e)}")


def _update_code(original_code: str, error_message: str, html_chunks: list, names: list, client) -> str:
    prompt = prompts['update_function_prompt'].format(
        function_code=original_code,
        error_message=error_message,
        names=names,
        html_chunks=html_chunks
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL,
    )
    updated_code = response.choices[0].message.content.strip()
    return _crop_code(updated_code)


def _crop_code(code: str) -> str:
    start_idx = code.find("```python") + len("```python") + 1
    end_idx = code.find('\n', code.find("return", start_idx)) + 1
    function_code = code[start_idx:end_idx]
    return function_code


def _chunk_html(html: str, block_size: int = 1000) -> list:
    chunks = []
    for i in range(0, len(html), block_size):
        chunks.append(html[i:i + block_size])
    chunk_sample = random.sample(chunks, min(10, len(chunks)))
    return chunk_sample


def _save_function(code: str, filepath: str) -> None:
    # logging.info(f"Saving generated function to {filepath}")
    with open(filepath, "w") as f:
        f.write(code)

# def execute_name_search_function(html_content: str, filepath: str) -> list:
#     try:
#         spec = importlib.util.spec_from_file_location("module.name", filepath)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
#         names = module.extract_phd_student_names(html_content)
#         return names
#     except Exception as e:
#         print("Parser module error:", e)
#         return []


if __name__ == "__main__":
    with open('scraper/urls.csv', 'r') as file:
        urls = [url.split(' ')[0] for url in file.readlines()]

    for url in urls:
        print("Processing URL:", url)
        html_source = requests.get(url).text
        generate_function(html_source, client, url)

# todo: if function confirmed by user create pull request, if not iterate
