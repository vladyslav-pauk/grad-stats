## Overview

This repository contains a Python project focused on scraping, processing, and viewing statistics related to PhD programs. The project is structured into two main components: `scraper` and `viewer`.

The `scraper` component is responsible for collecting data from various sources, processing it, and storing it in a usable format.

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

To get started with this project, follow the following steps.

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/paukvlad/Education.git
   cd Education/phd_stats
   ```

2. It is recommended to create a virtual environment to keep dependencies isolated:
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
      pip install -r viewer/requirements.txt
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

## Running the Code

### Python Environment

When running the components in a Python environment, you can interact with them directly.

#### Scraper

To run the scraper component:

```
python -m scraper
```

#### Viewer

To start the viewer web interface:

```
python viewer/src/app.py
```

The web interface will be accessible at `http://localhost:5000` by default.


### Using Docker

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
from scraper.src import data_processor, page_parser, snapshot_fetcher, update_placement, utils
```

To call the main scraper script from your Python script:

```python
import scraper

scraper.main()
```

### Viewer

The `viewer` package provides models and views for the web interface:

```python
from viewer.src import models, views, app
```

These modules can be used to extend or modify the web application.

## Webpage Interface

The `viewer` provides a web interface with the following features:

- A search form with autocomplete is provided for users to input a URL.
- Upon entering a URL and clicking the `Fetch` button, the website generates 
  a report.
- A button `Show/Hide Snapshots` allows users to toggle the visibility of 
  a table displaying URL time snapshots.

## Dataset

The dataset contains records of PhD candidates for a university department, 
detailing their academic and career progress. Key fields include:

- **Name**: Full name of the individual.
- **Snapshots**: URLs to archived Wayback Machine snapshots.
- **University**: Name of the university (e.g., 'arizona' for the University of Arizona).
- **Department**: Academic department or program.
- **Start_Date**: First record date in 'YYYY-MM-DD' format.
- **End_Date**: Last record date in 'YYYY-MM-DD' format.
- **Active**: Boolean indicating if the individual is still active in the department.
- **Years**: Duration of the individual's active period in the department (in years).
- **Placement**: Boolean indicating if the individual secured a placement or position post-tenure.

## Contributing

Contributions to this project are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Vladiszlav Pauk - paukvp@gmail.com

Project Link: https://github.com/paukvlad/Education
