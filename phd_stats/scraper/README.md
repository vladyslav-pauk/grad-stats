# README for scraper.py module

## Overview
This package is designed for web scraping, data processing, and dataset management.
It includes modules for fetching web page snapshots, parsing web pages for student data, and aggregating and summarizing the data.

## Installation

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Usage

To run the module, execute the following command from the root directory of the project:

```bash
python -m scraper [optional: path_to_urls_csv]
```

The optional `path_to_urls_csv` argument specifies the path to a CSV file containing URLs for scraping.

Upon execution, the module will fetch snapshots of the URLs, parse the web pages for student data, aggregate the new data into the dataset, and save the updated version of the dataset.

If no dataset is found, a new dataset will be created in the dataset folder located in the root directory of the project. 

## Modules Functionality
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
