# README for scraper.py module

## Overview
This package is designed for web scraping, data processing, and dataset management.
It includes modules for fetching web page snapshots, parsing web pages for student data, and aggregating and summarizing the data.

## Modules
- **data_aggregator.py**: Methods to process URL, aggregate student data, and calculate yearly metrics.
- **utils.py**: Methods to handle updating and managing dataset versions, including merging new data.
- **page_parser.py**: Methods to scrape web pages for student data, and extract metadata.
- **snapshot_fetcher.py**: A method to fetch snapshots of webpages from the Wayback Machine.
- **update_placement.py**: A method to update placement information from specified webpages.
- **__main__.py**: The entry point for the scraping and processing script.

## Installation
To run this project, ensure you have Python 3.x installed along with the following packages:
- pandas
- requests
- BeautifulSoup4
- re (regular expressions)

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Usage
### Running the Main Script
To run the module, execute the following command from the root directory of the project:

```bash
python -m scraper [optional: path_to_urls_csv]
```

The optional `path_to_urls_csv` argument specifies the path to a CSV file containing URLs for scraping.

### Modules Functionality
- **data_aggregator.py**
  - `clean_url(url: str)`: Cleans the archived URL to its original form.
  - `process_data(data: pd.DataFrame)`: Processes raw student data to create a summarized DataFrame.
  - `calculate_yearly_metrics(data: pd.DataFrame)`: Calculates and returns yearly metrics based on the data.

- **utils.py**
  - `update_dataset(new_data)`: Updates the dataset with new data.
  - `get_latest_version(data_folder='dataset')`: Retrieves the latest version of the dataset.
  - `merge_and_save(new_data, latest_version, data_folder='dataset')`: Merges and saves new data with the existing dataset.
  - `view_data(latest_data_path)`: Prints data from the latest dataset file.

- **page_parser.py**
  - `extract_timestamps(url: str)`: Extracts timestamps and metadata from a webpage.

- **snapshot_fetcher.py**
  - `get_snapshots(url: str, log: bool = False)`: Fetches Wayback Machine snapshots for a URL.

- **update_placement.py**
  - `update_placement_from_webpage(database_df: pd.DataFrame, url: str)`: Updates placement information from a webpage.

## Logging
The project utilizes Python's logging module for debugging and tracking. Ensure logging is appropriately set in each script to view detailed logs during execution.

## Notes
- Ensure you have network access for the modules to fetch data from URLs.
- The project does not handle all edge cases and exceptions; further development might be necessary for robustness.
- The effectiveness of data extraction depends on the structure of the target web pages.
