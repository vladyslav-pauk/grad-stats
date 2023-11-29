# Student Data Web Scraper and Viewer

This repository contains a set of Python modules for scraping, processing, and viewing student data from university web pages archived in the Wayback Machine. The project is split into two main components: the `scraper` and the `viewer`.

## Scraper

The `scraper` component is responsible for extracting student data from specified URLs, transforming it, and saving it for later analysis.

### Modules

- `data_scraper.py`: Defines the `scrape_data` function that takes a list of URLs and scrapes data from them.
- `data_processor.py`: Contains the `DataProcessor` class that processes raw data into a structured format.
- `page_parser.py`: Contains the `PageParser` class that parses individual web pages to extract student information.
- `snapshot_fetcher.py`: Contains the `SnapshotFetcher` class that fetches historical snapshots of web pages from the Wayback Machine.
- `data_explorer.py`: A script for displaying the number of snapshots for each student in a dataset.
- `update_placement.py`: A script to update the 'Placement' column in a dataset based on names found on a specified webpage.
- `utils.py`: Utility functions for managing dataset versions and merging data.

### Usage

To use the scraper, run the `__main__.py` module in the `scraper` directory with the required arguments. For example:

```bash
python -m scraper --url "https://example.com/students" --update
```

This will scrape data from the provided URL and optionally update an existing dataset if the `--update` flag is set.

## Viewer

The `viewer` component is a Flask web application that allows users to view and interact with the scraped data.

### Modules

- `app.py`: The entry point for the Flask application.
- `models.py`: Defines functions for loading and querying the dataset.
- `views.py`: Defines view functions for rendering web pages in the application.

### Usage

To run the viewer, navigate to the `viewer/src` directory and run `app.py`:

```bash
python app.py
```

The Flask application will start, and you can access it by visiting `http://localhost:5000/` in your web browser.

## Configuration

Both components use configuration files and paths that may need to be adjusted based on your environment:

- For the scraper, paths to datasets are configured within individual modules.
- For the viewer, `config.py` sets the path to the dataset used by the Flask application.

## Dependencies

This project requires several third-party libraries, including Pandas, BeautifulSoup, Requests, Flask, and ydata_profiling. Ensure all dependencies are installed before running the scraper or viewer.

## Contributing

Contributions are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is licensed under [LICENSE](LICENSE). Please see the LICENSE file for more details.