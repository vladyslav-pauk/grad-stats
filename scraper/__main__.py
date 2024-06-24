import argparse

import pandas as pd

from .src.program_page import get_page, get_pagination, scrape_data_from_pages
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
    # url_pairs = [('http://philosophy.princeton.edu:80/people/graduate-students',
    # 'https://philosophy.princeton.edu/graduate/placement-record')]


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


# todo: fix sorting
# todo: invalid dates

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
