# README

## Overview

This repository contains packages to scrape and view data on graduation and placement records of PhD students across philosophy programs in the USA.

The `scraper` module builds a dataset from open web sources.

The `viewer` component provides a web interface to visualize and interact with the collected data.

You can run the `scraper` and `viewer` components in a Python environment or 
as Docker containers, as well as use them as Python packages.

## Installation

### Requirements

Before you begin, ensure you have the following installed on your system:

- git
- Python 3.x
- Docker (optional)
- Docker Compose (optional)

### Setting Up the Environment

To get started, follow these steps:

#### Install Python Environment

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/paukvlad/phd-stats.git
   cd phd-stats
   ```

2. It is recommended to create a virtual environment to keep dependencies isolated:

   On macOS and Linux, use:
   ```
   python -m venv venv
   source venv/bin/activate 
   ```
   On Windows use:

   ```
   venv\Scripts\activate
   ```

3. Install the required Python packages:
   
      ```
      pip install -r scraper/requirements.txt
      ```

#### Install JavaScript Environment

1. Navigate to the project root directory and install the required JavaScript packages:
   ```
   npm install
   ```


### Using Docker

If you prefer using Docker, you can build the Docker image and run containers using the provided `docker-compose.yml`.

Before running these commands, ensure that Docker is installed and the Docker daemon is running on your machine. You can usually start the Docker daemon through your system's service management (like `systemctl start docker` on Linux) or simply by opening the Docker Desktop application if you're on Windows or macOS.

1. Build the Docker images using Docker Compose:
   ```
   docker-compose build
   ```

2. Start the services using Docker Compose:
   ```
   docker-compose up -d
   ```
   
You can also run the `scraper` and `viewer` services individually using `docker-compose up scraper` and `docker-compose up viewer`, respectively.

## Usage

### Scraper

The `scraper` module is designed for scraping web data into a  dataset.

Run the module upon installation using the following command from the root directory of the project:

```bash
python -m scraper
```

The module will start fetching time snapshots of the URLs, parse the web pages for student data, and aggregate the new data and save the updated version of the dataset.

See more details in the `scraper` module README.

### Dataset

The dataset contains records of PhD candidates for a university department, 
detailing their academic and career progress. Key fields include:

- **Snapshots**: URLs to archived Wayback Machine snapshots.
- **University**: Name of the university (e.g., 'arizona' for the University of Arizona).
- **Department**: Academic department or program.
- **Start_Date**: First record date in 'YYYY-MM-DD' format.
- **End_Date**: Last record date in 'YYYY-MM-DD' format.
- **Active**: Boolean indicating if the individual is still active in the department.
- **Years**: Duration of the individual's active period in the department (in years).
- **Placement**: Boolean indicating if the individual secured a placement or position post-tenure.

### Browser App

The `viewer` provides a web interface for accessing and analysing data with the following key features:

- **DataTable Profiling**: Generates a detailed statistical profiling using `pandas` library.
- **Program Filtering**: Facilitates filtering by PhD programs.
- **Snapshot Viewing**: Displays links to the source snapshots of data on the https://web.archive.org.

See the `viewer` module README for more details.


### Running in Python Environment

When running the components in a Python environment, you can interact with them directly.

To run the scraper component:

```
python -m scraper
```

To start the viewer web interface:

```
python viewer/src/app.py
```

The web interface will be accessible at `http://localhost:5000` by default.


### Running Using Docker

Once the Docker containers are up and running, you can interact with the `scraper` and `viewer` services.

#### Scraper

The `scraper` is responsible for collecting data from various sources. To use it:

1. Access the `scraper` Docker container:
    ```bash
    docker-compose run scraper /bin/bash
    ```

2. Inside the container, run the `scraper` as a module:
    ```bash
    python -m scraper
    ```
   
After the scraper completes, the collected data will be stored in the Docker 
volume `phd_stats_dataset`.
It will be accessible from the host machine at `./dataset` by default.
From the terminal, you can access the volume using the following command:

```bash
docker volume inspect phd_stats_dataset
```

#### Viewer

The `viewer` provides a web interface to display the collected data. To access it:

1. Ensure the `viewer` service is running as part of the Docker Compose setup.
2. Open a web browser and navigate to `http://localhost:5000` or the 
   configured port.

## Using as Python Packages

To use `scraper` and `viewer` as Python packages, you'll need to install them in your environment.

1. Navigate to the respective directories:
    ```bash
    cd phd_stats/scraper
    cd phd_stats/viewer
    ```

2. Install the packages using pip:
    ```bash
    pip install .
    ```

After installation, you can import modules from these packages in your Python scripts.

### Scraper

The `scraper` package can be imported into your Python scripts as follows:

```python
from scraper.src import data_processor, program_page, snapshot_url, update_placement, utils
```

To call the main scraper script from your Python script:

```python
import scraper
scraper.main()
```

## Viewer

The `viewer` package provides models and views for the web interface:

```python
from temp.viewer import views
from temp.viewer.src import app, models
```

These modules can be used to extend or modify the web application.

## Contributing

Contributions to this project are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Notes

- The package does not handle all edge cases and exceptions; further development might be necessary for robustness.
- The effectiveness of data extraction depends on the structure of the target web pages.
- Ensure you have network access for the modules to fetch data from URLs.
- The viewer is designed to work with the dataset generated by the `scraper` module.

## Contact

Vladyslav Pauk - paukvp@gmail.com

Project Link: https://github.com/paukvlad/Education
