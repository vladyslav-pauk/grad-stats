# Scraping Web for Academic Progress

The data scraping module is an efficient tool for gathering information about changes in graduate student enrollment over time from university websites.
It aims at streamlining the data collection process by leveraging Wayback Machine web archive service and automatic pattern matching generation using OpenAI's GPT API.

[//]: # (The PhD program scraping module addresses this challenge by automating the extraction of PhD student names from university web pages.)

## Table of Contents

1. [Overview](#overview)

   1.1 [Archive of Enrollment Data](#archive-of-enrollment-data)

   1.2 [Challenges in Data Collection](#challenges-in-data-collection)

2. [Methodology](#methodology)

   2.1 [Enrollment Duration](#enrollment-duration)

   2.2 [Accuracy and Reliability](#accuracy-and-reliability)

   2.3 [Automatic Code Generation](#automatic-code-generation)

   2.4 [Efficiency and Reliability](#efficiency-and-reliability)

3. [Architecture](#architecture)

   3.1 [Code Generation Pipeline](#code-generation-pipeline)

   3.2 [Dataset Structure](#dataset-structure)

4. [Implementation](#implementation)

   4.1 [Error-Driven Design](#error-driven-design)

   4.2 [Wayback Machine Integration](#wayback-machine-integration)

   4.3 [Code Generation](#code-generation)

   4.4 [Parsing Web Page Source](#parsing-web-page-source)

   4.5 [Scraping Schedule](#scraping-schedule)

## Overview

Enrollment, graduation and placement data for graduate programs is a valuable resource for academic research, program evaluation, student recruitment, and ranking.
Across various disciplines, data reporting varies in terms of consistency and accessibility.
Centralized databases like the [National Science Foundation's Survey of Earned Doctorates](https://ncses.nsf.gov/surveys/earned-doctorates) provide aggregate statistics, but lack information on individual programs.
Some grant-funded initiatives like the [Council of Graduate Schools' PhD Completion Project](https://cgsnet.org/data-insights/diversity-equity-inclusiveness/degree-completion/ph-d-completion-project) aim to improve data collection and reporting, but challenges remain.
Such initiatives are labor-intensive and require manual updating. 
They may not capture the full range of programs and outcomes and often not up-to-date.
Furthermore, accessing this data directly from the educational institutions can be challenging due to legacy systems, privacy concerns, and inconsistent reporting practices.

### Archive of Enrollment Data

University academic departments often publish lists of current graduate students on their websites, providing insights into the student body of individual programs.
Philosophy programs, for example, often provide detailed information on current graduate students, including their names, graduation status, and placement outcomes.

The Wayback Machine web archive service captures snapshots of web pages over time, which enables tracking changes in student listings, and enables longitudinal analysis of enrollment.
By monitoring student names in the webpage over time, one can estimate start and end dates of each student's enrollment, providing access to time-to-degree metrics.
Finally, to assess the outcomes for each student, the placement and graduation information can be retrieved by matching student database against program placement, alumni and other open sources.

### Challenges in Data Collection

Collecting web archive data on graduate students is a challenging task due to the lack of standardized formats and the dynamic nature of web content.
Using standard web scraping techniques and libraries yields limited results due to the variability in webpage structures and internationalization of names.
Furthermore, webpages often list supervisors, alumni, and other non-student names, further complicating the extraction process.
Manual programming of pattern matching is time-consuming, requires handling of edge cases, is not scalable to a large number of academic programs, and requires manual maintenance and updates.

Recent progress in Large Language Models (LLMs) opens up new avenues for automating the extraction of content from web pages.
LLMs like OpenAI's GPT demonstrate remarkable capabilities in information retrieval and generation tasks, and become a widespread tool for various NLP tasks in industry and academia.
At the same time, the non-deterministic nature of LLMs poses challenges for generating reliable results when used directly for information retrieval.
Furthermore, inference with LLMs is computationally expensive when applied to large corpora of web pages which may result in a significant overhead.

## Methodology

### Enrollment Duration

We estimate student enrollment in a program over time based on the student’s first and last appearances in the web page source.
The actual enrollment date is not available and is uncorrelated with the snapshot frequency.
It is assumed to occur between the time of the first appearance and the preceding snapshot.
In case the first appearance is the first snapshot, the start date is not available.
The end date is estimated to be sometime after the last appearance but before the next snapshot.
The duration of the program for each student is calculated as the time elapsed between the estimated start and end dates, given both are available.

If a student is currently listed on the program webpage it is assumed to be active and the end date is not available.
We don't consider graduation rate in this module, however our approach can be extended to include this metric.

We estimate the average time-to-degree for the program by calculating the mean duration of all past students.
Note, that this definition assumes that all students graduated, which may not be the case.
By extending our model with the graduation information, this can be straightforwardly addressed.
We don't include the current students in calculating the average time-to-degree, as recent students may introduce bias towards shorter durations.

### Accuracy and Reliability

We make several assumptions to estimate the enrollment duration and program completion:
- The student's name is listed on the program webpage at least once during their enrollment.
- The student's name is listed on the program webpage only while they are enrolled.
- The extracted current students did not graduate yet.
- A student's name is a unique identifier.
- Program and placement pages are up-to-date and accurate.
- The start (end) date are estimated as the date of the first (last) snapshot where the student is listed.

Since our aim is estimating cumulative enrollment and duration of the program, rather than individual student data, the assumptions are reasonable and do not significantly affect the overall accuracy of the analysis.
Philosophy programs are typically accurate in listing current students and placement records, and the data is often updated regularly.
Name collisions are rare.

Besides currently enrolled students, the web page may list faculty, alumni, or students who have already graduated.
To address this, we design the search functions so that they target the currently active students specifically, filtering out other entities. 
With a minimal intervention, we can increase accuracy of the name search by manually validating the extracted names as a part of the generation pipeline.

The frequency of snapshot captures varies per website. Websites in the "Worldwide Web Crawls" are included in a "crawl list", with the site archived once per crawl. A crawl can take months or even years to complete, depending on size.
See [Wikipedia](https://en.wikipedia.org/wiki/Wayback_Machine) and [Wayback Machine Help](https://help.archive.org) for more information.

### Automatic Code Generation

We propose a hybrid approach that combines the strengths of LLMs with programmatic pattern matching, and facilitates automating the process of extracting information from non-standardized web pages.
By leveraging OpenAI's GPT API, we streamline generation of Python functions that extract names from web page sources, providing a scalable and adaptable solution for data collection, while maintaining robustness and reliability of programmatic extraction.

The core of the module's methodology is the use of OpenAI's GPT API to generate Python functions for name extraction.
Using GPT-generated functions offers a non-deterministic solution providing means for automatic adaption to changes in the web page structure.
This approach is agnostic to the specific structure of web pages, making it adaptable to various non-standardized sources.
The generated functions are deterministic, providing robustness and reproducibility in the extraction process.

[//]: # (Using a prompt designed to create a function that identifies all unique PhD student names on a given web page.)

[//]: # (The generated code is then saved as a Python file and executed to extract the names.)

### Efficiency and Reliability

Using GPT for code generation, rather than relying on direct inference, mitigates the overheads associated with traditional NLP model approaches, which require iterative execution of resource-intensive models on extensive datasets. Additionally, pattern matching is computationally efficient.

Generated code undergoes programmatic validation to ensure it meets the required functionality and correctness. To enhance robustness and reliability, users are prompted to verify the correctness of the generated code. If the generated function returns incorrect results, users can provide feedback to the model, facilitating continuous improvement.
For each generated function, the user only needs to inspect the extracted names once to verify the correctness of the code.


[//]: # (At the same time, using programmatic pattern matching provides an efficient and scalable solution for extracting information from large html sources.)

[//]: # (### Automation and Adaptability)

The pipeline can automatically adjust to changes in web page structures by re-running the generation process, eliminating the need for manual updates and reducing maintenance demands.
By modifying the prompt, this approach can be easily adapted to a specific task.
We can target specifically graduate students, or generally, students with specific traits.
This is difficult to achieve using NLP models or generic pattern matching without hand-crafted rules.

## Architecture

The module architecture is based on three main components: extracting webpage source of snapshots from the web archive, generating Python functions to extract names from the source, and building a database of student information based on extracted data.

The list of Wayback Machine snapshot URLs is obtained with `snapshot_url.py` module.
The `program_page.py` module handles fetching and processing data from snapshots of web pages.
These two modules interact with the Wayback Machine API to retrieve the archived web pages. 

The student information is retrieved using the `searn_names.py` module which calls generated search modules to extract names from the source.
The placement information is retrieved using the `placement_page.py` module which fetches and processes data from the placement pages.
The extracted data is processed and stored in a structured format in the database by `database.py` module.

The search modules are generated with `module_manager.py`. The module interacts with the OpenAI API to generate Python functions via `gpt_api.py` module.
The validation of the generated functions is performed by verifying extracted names.
This is implemented in `student_mame.py` module, which handles both programmatic validation and interaction with the user via command line interface.

### Code Generation Pipeline

The challenges arising related to non-determinism of GPT-based coding are handled via a feedback loop between validation and generation processes.

The pipeline for code generation involves the following steps:

[//]: # (1. **Validation**: The `search_module` is validated using the `validate_function`.)

[//]: # (   - If validation passes, data scraping from archive snapshots proceeds.)

[//]: # (   - If validation fails, the code is generated using `generate_code`.)

[//]: # ()
[//]: # (2. **Code Generation**: A function is generated to extract names from the web page source using `generate_code`.)

[//]: # (   - The generated code is validated with `validate_function`.)

[//]: # (   - If validation passes, the code is saved as a Python file.)

[//]: # (   - If validation fails, the code is updated using `update_code` and revalidated.)

[//]: # (3. **Update Code**: The code is updated based on the chat response and saved to a Python file.)

[//]: # (   - The updated function is validated and saved to a Python file.)

[//]: # (   - The process is repeated until the function is validated.)

- validate `search_modules/<module>` with `module_manager.validate_function`. 
  - if passed, proceed to scraping data from the archive snapshots.
- otherwise, generate the code to extract names from the web page source with `module_manager.generate_function`
  - validate the generated code with `module_manager.validate_function`
    - if passed, save the updated code to a Python file.
- otherwise, update code with `module_manager._update_code`
  - append the validation result to the chat history and pass it back to the chat
  - update the search function from the chat response and save it to a Python file
  - validate updated function and save it to a Python file
    - repeat until the function is validated

[//]: # (### Modularity)

[//]: # ()
[//]: # (The module is divided into distinct components, each handling specific tasks such as code generation, validation, data processing, and error handling. This modularity ensures ease of maintenance, scalability, and flexibility.)


### Dataset Structure

The extracted data is stored in a structured format in `public/data/student_data_v<version>.json` with the following schema:

```
dataset (<u>name</u>, university, url, start_date, end_date, active, years, snapshots, placement)
```

where:
- <u>`name`</u> (str): Full name, primary key of the dataset
- `university` (str): Host university
- `url` (str): Current graduate students page
- `placement_url` (str): Placements page
- `start_date` (str): Start date of the program
- `end_date` (str): End date of the program
- `active` (bool): Whether the student is currently enrolled
- `years` (int): Duration of the program in years
- `snapshots` (list): URLs of snapshots
- `placement` (bool): Whether the student has a placement

The primary program identifier is the domain name of the university.

#### Example JSON Entry

```json
{
  "Name": "Brandon Beaver",
  "University": "Oregano State University",
  "URL": "https://philos.oregano.or/graduate-programs/graduate-students",
  "PlacementURL": "https://philos.oregano.or/graduate-programs/placements",
  "Start_Date": "2020-01-10 00:00:00",
  "End_Date": "2024-06-17 00:00:00",
  "Active": true,
  "Years": 0.0,
  "Snapshots": [
    "https://philos.oregano.or/graduate-programs/graduate-students/",
    "https://web.archive.org/web/20200110000000/https://philos.oregano.or/graduate-programs/graduate-students/"
  ],
  "Placement": false
}
```

After extracting the data, it is matched against the most recent database version to identify new entries.
The new entries are then added to the database, and the database version is updated.

## Implementation

### Error-Driven Design

The implementation of the module is built around efficient error handling, which plays a crucial role in the code generation and validation process.
The program involves invoking machine-generated code, which may not always be correct or exhibit the desired behavior or structure.
By utilizing exceptions, the architecture efficiently handles the non-deterministic nature of the system and facilitates seamless interaction between the program and the chat API.

If a function fails validation, it is treated as an exception, and the error is propagated to the GPT API for context-aware function generation.
This approach allows for unified handling of validation, module, and server errors within a single feedback interface.

In the `exceptions.py` module, we define custom error classes: `ModuleError`, `ValidationError`, `OpenAIError`, and `WaybackMachineError` to categorize errors from different modules. `ModuleError` and `ValidationError` are redirected to the chat API to update the context for function generation. `OpenAIError` and `WaybackMachineError` are logged and displayed to the user.

### Wayback Machine Integration

The module integrates with the Wayback Machine to retrieve archived snapshots of web pages.
The `snapshot_url.py` module first checks for the availability of snapshots for the given URL and then fetches and parses all available snapshots.
A retry mechanism is implemented to handle temporary connection and server errors.

In Wayback Machine web archive, snapshots of documents and resources are stored with time stamp URLs such as `20240615142741`.
The date of the snapshot is encoded in the URL, allowing for easy retrieval of the snapshot date.


[//]: # ([Leetaru, Kalev &#40;January 28, 2016&#41;. "The Internet Archive Turns 20: A Behind the Scenes Look at Archiving the Web". Forbes.]&#40;https://www.forbes.com/sites/kalevleetaru/2016/01/18/the-internet-archive-turns-20-a-behind-the-scenes-look-at-archiving-the-web/#222f2e5682e0&#41;)


### Code Generation

The interaction with the OpenAI API is managed by the `gpt_api.py` module via predefined prompts.
The prompts for the GPT model in `prompts.yaml` are designed to generate a function that extracts all unique graduate student names from a web page source. It includes the function signature and a high-level description of the required functionality.

```yaml
setup_prompt: |
  
  You are an expert in Python and web scraping using BeautifulSoup, HTML, regex and other libraries.
  
  You have to follow instructions and respond to prompts as precisely as possible.


generate_function_prompt: |

  Your task is to create a function that extracts a list of current PhD student names from an HTML source.
   The function should be named `extract_phd_student_names` and should take a BeautifulSoup object as input, returning a list of strings where each string is a current PhD student's name.
   Make sure it only selects all current students.
  
  Analyze the following HTML source chunks to understand the structure of the web page:
  
  {html_chunks}

  Based on the structure and patterns identified in the provided HTML source chunks, write the `extract_phd_student_names` function. Make sure to include the necessary import statements.

  ### Expected Response 

  def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
      # Your code here

  
  This function accurately extracts the names of current PhD students based on the status specified and all information provided in the HTML source.


update_function_prompt: |

  Your task is to update the function `extract_phd_student_names` to fix incorrect behavior.
  You must use matching patterns and HTML structures in the source.
  
  The function signature should be `extract_phd_student_names(source: BeautifulSoup) -> list[str]`.
  In your response, provide only the code with the function and necessary import statements included.
  
  Names extracted by the previous implementation:
  {names}
  
  Error message:
  {error_message}
  
  I expect your response to include the following structure:
  
  from bs4 import BeautifulSoup
  
  def extract_phd_student_names(source: BeautifulSoup) -> list[str]:
      <your code here>
      return students

  This update ensures that the function accurately extracts the names of current PhD students.

```

These prompt is tailored to generate patterns specifically targeting current graduate student names, avoiding names of faculty or alumni.

The response from the GPT model is processed to extract the relevant code within code block markers. The code is then trimmed after the return statement to ensure functionality.

### Parsing Web Page Source

Some pages include pagination.
The `program_page.py` module manages it by sequentially extracting names from all pages, using incremental page numbers in the pagination URL query strings (e.g., `?pg=1`). This process continues until no new pages are detected or the page content is empty.

The raw HTML content is parsed using the BeautifulSoup library and then broken down into chunks.
We randomly sample and present a subset of these chunks to the GPT model for analysis and pattern generation.
Sampling has two benefits are two-fold: it provides a representative view of the page structure and reduces the computational load on the model.
In fact, the entire page source won't fit into the GPT model's token limit, so sampling is necessary.

### Scraping Schedule

The module processes the programs from `public/programs.csv` file and updates the database after each program scan with new records.
In this way that the new data is saved incrementally, allowing for easy tracking of changes and updates.
In case of errors, the module logs the error and continues with the next program, ensuring the scraping process is robust and fault-tolerant.
Users can monitor the progress and status of the scraping process through the logs, validation output, and the database viewer.
When needed the module can be run for a specific program or a set of programs, allowing for targeted data collection and correction.
