# Web Scraping Module

This repository contains a robust and scalable web scraping module designed to extract PhD student information from university program pages. Leveraging Python, BeautifulSoup, and GPT-based code generation, this module ensures efficient data extraction, validation, and processing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Modules](#modules)
  - [Main Script](#main-script)
  - [Database Module](#database-module)
  - [Exception Handling](#exception-handling)
  - [GPT API](#gpt-api)
  - [Module Manager](#module-manager)
  - [Placement Page](#placement-page)
  - [Program Page](#program-page)
  - [Search Module](#search-module)
  - [Snapshot URL](#snapshot-url)
  - [Student Name](#student-name)
  - [Utilities](#utilities)
- [Contributing](#contributing)
- [License](#license)

## Overview

This module automates the extraction and processing of PhD student information from university websites. It utilizes a combination of web scraping techniques and GPT-generated code to ensure accuracy and efficiency.

## Features

- **Automated Data Extraction:** Extracts PhD student names and related data from program pages.
- **Data Validation:** Ensures the extracted data is accurate and complete.
- **GPT Integration:** Generates and updates scraping functions using GPT.
- **Comprehensive Logging:** Logs all operations and errors for easy debugging and auditing.
- **Modular Design:** Organized into distinct modules for easy maintenance and extension.

## Installation

Ensure you have Python installed, and create a virtual environment.
On macOS and Linux, use:

```bash
python -m venv venv
source venv/bin/activate 
```

Then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The primary entry point for this module is the `__main__.py` script. It reads a CSV file containing program URLs and processes the data.

Run the script as follows:

```bash
python -m scraper <path_to_url_file>
```

For example:

```bash
python -m scraper public/urls.csv
```

## Directory Structure

```
.
├── __init__.py
├── __main__.py
├── src
│   ├── __init__.py
│   ├── search_modules
│   │   ├── module_1.py
│   │   ├── module_2.py
│   │   └── ...
│   ├── config.json
│   ├── database.py
│   ├── exceptions.py
│   ├── gpt_api.py
│   ├── module_manager.py
│   ├── placement_page.py
│   ├── program_page.py
│   ├── prompts.yaml
│   ├── search_module.py
│   ├── snapshot_url.py
│   ├── student_name.py
│   └── utils.py
└── README.md
```

## Modules

### Main Script

#### `__main__.py`

The `__main__.py` script is the central orchestrator. It manages the flow of reading URLs, validating and generating search modules, and processing data.

```python
import argparse
import pandas as pd
from src.module_manager import generate_search_module, validate_search_module
from src.program_page import get_page, get_pagination, add_data_from_pages
from src.placement_page import update_placement
from src.database import update_dataset
from src.utils import read_programs, load_logging
from src.exceptions import ValidationError, ModuleError

def main(filename: str) -> pd.DataFrame:
    programs = read_programs(filename)
    data = pd.DataFrame()

    for program in programs:
        load_search_module(validation_url=program[0])
        pagination = get_pagination(program)
        data = add_data_from_pages(data, program, page_urls=pagination)
        data = update_placement(data, placement_page=program[1], log=False)
        update_dataset(data)

    return data

if __name__ == '__main__':
    load_logging()
    parser = argparse.ArgumentParser(description="Scrape appearance data and update placement.")
    parser.add_argument("file", nargs='?', default="public/urls.csv", type=str, help="The file with URLs.")
    args = parser.parse_args()
    new_data = main(args.file)
```

### Database Module

#### `database.py`

Handles updating, processing, and viewing the dataset of student information.

```python
def update_dataset(new_data: pd.DataFrame) -> None
def process_data(data: pd.DataFrame, log: bool) -> pd.DataFrame
def view_data(latest_data_path: str) -> None
def calculate_yearly_metrics(data: pd.DataFrame) -> pd.DataFrame
```

### Exception Handling

#### `exceptions.py`

Defines custom exception classes for specific error types.

```python
class ValidationError(Exception)
class ModuleError(Exception)
class OpenAIError(Exception)
class WaybackMachineError(Exception)
def handle_exception(exc_type, exc_value, exc_traceback) -> None
```

### GPT API

#### `gpt_api.py`

Interacts with the GPT API to generate and update search modules.

```python
def get_gpt_response(gpt_chat: tuple, prompt: str) -> str
def init_gpt_chat() -> tuple
```

### Module Manager

#### `module_manager.py`

Generates, validates, and updates search modules using GPT responses.

```python
def generate_search_module(html_source: str, url: str) -> None
def validate_search_module(html_source: str, url: str) -> bool
```

### Placement Page

#### `placement_page.py`

Updates the 'Placement' column in the database with names found on the placement webpage.

```python
def update_placement(database_df: pd.DataFrame, placement_page: str, log: bool = True) -> pd.DataFrame
```

### Program Page

#### `program_page.py`

Handles data extraction from paginated web pages.

```python
def add_data_from_pages(data, program_tuple, page_urls) -> pd.DataFrame
def get_pagination(url_tuple) -> List[str]
def get_page(url: str, max_retries: int = 10, initial_retry_delay: int = 16) -> str
```

### Search Module

#### `search_module.py`

Searches for names in HTML content using dynamically loaded search modules.

```python
def search_names(html_content: str, url: str) -> List[str]
```

### Snapshot URL

#### `snapshot_url.py`

Fetches Wayback Machine snapshots for a given URL with a retry mechanism.

```python
def get_snapshot_urls(url_tuple: Tuple[str], max_retries: int, retry_delay: int, log: bool = False) -> List[str]
```

### Student Name

#### `student_name.py`

Validates a list of names against the provided source content.

```python
def validate_names(source: str, name_list: List[str]) -> bool
```

### Utilities

#### `utils.py`

Provides utility functions for configuration, system path management, logging setup, and more.

```python
def load_config() -> tuple
def load_sys_path() -> None
def load_logging() -> None
def load_nltk() -> None
def read_programs(filename: str) -> list
def parse_module_name(url: str) -> tuple
def parent_url(url: str) -> str
```

## Contributing

We welcome contributions from the community. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
