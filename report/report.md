## Methodology

Programming name search in a web page source was streamlined using OpenAi's GPT API.
We use a prompt to generate a function with a given signature, that finds all unique PhD student names in a given web page source.
The code is then saved as a Python file and executed to extract the names.
We can then run a scraping schedule that will iterate through all the methods of the search module.
The metadata such as the URL are stored as a part of the function signature.
When generated the function is tested in a test module before being saved.

Using GPT API we generate code for name extraction from a web page source.
For each generated function, the user only needs to inspect the extracted names once to verify the correctness of the code.
Given that the structure of the web page source is not updated frequently, the generated code is expected to be robust and reliable after verification.
By using generated functions we reduce overheads from using language models to extract names from web pages while maintaining the robustness, flexibility and scalability of the code.
The user doesn't need to install heavyweight models.

### Prompting

The prompt is designed to generate a function that extracts all unique PhD student names from a web page source.
The function signature as well a high-level description of the architecture is given as an argument to the prompt.
We use the following prompt to generate the function:

```text
Provide python code for the following README.
```

## Signature

`generate_name_search_function(url: str, source: str) -> str`
` is the function that generates the code to extract the names from a web page source.

`save_name_search_function(code: str, url: str) -> None`
` is the function that saves the generated code to a Python file with the given URL as the file name.

`execute_name_search_function(url: str) -> List[str]`
` is the function that executes the generated code to extract the names from the web page source by iterating through all the methods of the search module.