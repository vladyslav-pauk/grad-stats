import argparse

import pandas as pd

from .src.module_manager import generate_search_module, validate_search_module
from .src.program_page import get_page, get_pagination, add_data_from_pages
from .src.placement_page import update_placement
from .src.database import update_dataset
from .src.utils import read_programs, load_logging
from .src.exceptions import ValidationError, ModuleError


def main(filename: str) -> pd.DataFrame:
    """
    Main function to scrape data for a list of programs.

    Args:
        filename (str): The file with program URLs.
    Returns:
        pd.DataFrame: The object with scraped data.
    """
    programs = read_programs(filename)
    data = pd.DataFrame()

    for program in programs:
        load_search_module(validation_url=program[0])
        pagination = get_pagination(program)
        data = add_data_from_pages(data, program, page_urls=pagination)
        data = update_placement(data, placement_page=program[1], log=False)
        update_dataset(data)

    return data
    # url_pairs = [('http://philosophy.princeton.edu:80/people/graduate-students',
    # 'https://philosophy.princeton.edu/graduate/placement-record')]


def load_search_module(validation_url):
    """
    Validate or generate the search function.

    Args:
        validation_url: The URL to validate the function.
    Returns:
        None
    """
    validation_html = get_page(validation_url)
    try:
        validate_search_module(validation_html, validation_url)
    except (ValidationError, ModuleError):
        generate_search_module(validation_html, validation_url)
    # save snapshot items to a text file
    # with open('scraper/tests/snapshots.csv', 'w') as file:
    #     for url in snapshot_urls:
    #         file.write(url + '\n')

    # with open('scraper/tests/validation_2024-06-09.html', 'r') as file:
    #     validation_html = file.read()
    #
    # with open('scraper/tests/snapshots.csv', 'r') as file:
    #     snapshot_urls = file.read().splitlines()

    # with open(f'scraper/tests/validation_{parse_date(url)[0]}.html', 'r') as file:
    #     page_source = file.read()


if __name__ == '__main__':
    load_logging()

    parser = argparse.ArgumentParser(
        description="Scrape appearance data and update placement."
    )
    parser.add_argument(
        "file",
        nargs='?',
        default="public/programs.csv",
        type=str,
        help="The file with URLs."
    )

    args = parser.parse_args()

    if args.file is None:
        new_data = main('../public/programs.csv')
    else:
        new_data = main(args.file)


# todo: README
# todo: report

# viewer
# todo: more statistics in program summary, also some metadata

# fixme: nav tabs, border-bottom
# fixme: tooltip transparency
# fixme: align tooltip window to the left
# fixme: fix sorting indicator initialization and memory

# scraper
# todo: calculate start date and end date in the middle between two snapshots
#  keep start_date and end_date as it is but use ranges for calculating average
#  end_date should be the last snapshot before disappeared. if it's active no end-date.
# todo: pass error e to chat, but log only error info.
# todo: validation feedback
# todo: if function confirmed by user create pull request, if not iterate
# todo: function to delete entries from database

# fixme: context length error
# fixme: log every page, log at the end of url search
# fixme: handle empty name list, possible for pagination
# fixme: update function before first page, don't update further
# fixme: fix placement (wrong student, o'hagan)
