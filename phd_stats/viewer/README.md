# README for PhD Stats Web Application

## Overview
The PhD Stats Web Application is designed to assist in the chronological profiling of PhD programs from various universities across the United States. It provides an interface for users to search and view statistical data on PhD programs.

## Key Features
- **URL Search**: Allows users to search for specific URLs related to PhD programs.
- **Data Profiling**: Generates profiling reports for selected URLs.
- **Snapshot Viewing**: Displays historical snapshots of data for comparative analysis.

## Installation and Setup
### Prerequisites
- Python 3.x
- Flask
- Other Python packages as listed in `requirements.txt`

### Installation Steps
1. Clone the repository to your local machine.
2. Install the required Python packages using the command:

    ```pip install -r requirements.txt```

3. Navigate to the root directory of the project.

### Configuration
- Update `config.py` with the necessary configuration settings.
- Place your dataset in the specified data folder (default: `dataset`).

## Running the Application
To run the application:
1. Execute `app.py`:
    
    ```python app.py```

2. The application will start on the configured host and port, defaulting to `0.0.0.0:5000`.

## Using the Application
- Access the application through a web browser at `http://<HOST>:<PORT>`, where `<HOST>` and `<PORT>` are your configured settings.
- Use the URL search feature to find and select a URL.
- View the generated profiling report and snapshots for the selected URL.

## Structure
- `app.py`: Main Flask application setup and routes.
- `models.py
