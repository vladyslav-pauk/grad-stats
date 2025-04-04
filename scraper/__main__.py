import argparse

import pandas as pd

from .src.program_page import get_pagination, scrape_data_from_pages
from .src.placement_page import update_placement
from .src.database import update_dataset
from .src.utils import read_programs, load_logging


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

    for program_tuple in programs:
        pagination = get_pagination(program_tuple)
        data = scrape_data_from_pages(data, program_tuple, page_urls=pagination)
        data = update_placement(data, placement_page=program_tuple[1], log=False)
        update_dataset(data)

    return data


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

# todo: report

# viewer

# fixme: nav tabs, border-bottom
# fixme: tooltip transparency

# scraper

# fixme: fix placement

# todo: delete a program command

# todo: pass error e to chat, but log only error info
# todo: prompt only if name list changed
# todo: update only placement
# todo: add graduate page to the program tuple
# todo: log every page, log at the end of url search
# todo: handle empty name list, possible for pagination
# todo: fix placement (wrong student, o'hagan)
