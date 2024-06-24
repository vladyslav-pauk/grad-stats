# PhD Stats

## Overview

The PhD Stats is a React application designed to provide an interactive interface for exploring and analyzing data related to PhD programs. It allows users to search for universities, view detailed statistics on student data, and gain insights into various programs.

## Features

### Search Functionality

- **Search Bar**: The search bar at the top of the application allows users to search for universities by typing the name of the university or program. As you type, a dropdown list of matching universities will appear.
- **Dropdown Navigation**: Use the arrow keys to navigate through the dropdown list and press enter to select a university. Clicking on a university name in the dropdown will display the statistics for that university.
- **Automatic Suggestions**: If the search query is empty and the search bar is focused, a list of all available programs will be displayed.

### Tabs

The application features multiple tabs to display different types of data:

- **Graduate Programs**: Shows a summary of various PhD programs, including total entries, currently active students, placement rates, etc. Clicking on a program name will display detailed statistics for that program.
- **Summary**: Provides a detailed summary of the selected program, including the number of currently enrolled students, total students recorded, placement rate, average time-to-degree, and more.
- **Student Data**: Displays detailed student data for the selected program, including student names, enrollment dates, completion dates, time to degree, and placement status.
- **Snapshots**: Shows links to snapshots of the program data, including the date of the snapshot and the number of students listed in the snapshot.

### Sorting

- **Sortable Columns**: Users can sort the data in the tables by clicking on the column headers. The columns can be sorted in ascending or descending order. The current sort direction is indicated by an arrow next to the column header.

### Tooltips

- **Informative Tooltips**: Hovering over the column headers in the tables will display tooltips with additional information about the column. This helps users understand the meaning of each column and the data it represents.

### Click to Proceed

- **Program Selection**: Clicking on a program name in the Graduate Programs tab or a university name in the search dropdown will display detailed statistics for that program or university.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/paukvlad/phd-stats.git
```

2. Navigate to the project directory:

```sh
cd phd-stats
```

3. Install the dependencies:

```sh
npm install
```

4. Start the development server:

```sh
npm start
```

The application will be available at `http://localhost:3000`.

## Usage

### Search

1. **Type in the Search Bar**: Start typing the name of a university or program in the search bar.
2. **Navigate the Dropdown**: Use the arrow keys to navigate the dropdown list of universities. Press enter to select a university or click on the university name.
3. **View Program Statistics**: Once a university is selected, the detailed statistics for that program will be displayed.

### Tabs

1. **Graduate Programs Tab**: Displays a summary of various PhD programs. Click on a program name to view detailed statistics for that program.
2. **Summary Tab**: Provides a detailed summary of the selected program, including statistics like currently enrolled students, placement rates, and average time-to-degree.
3. **Student Data Tab**: Displays detailed student data for the selected program. You can sort the data by clicking on the column headers.
4. **Snapshots Tab**: Shows links to snapshots of the program data. The snapshots include the date and number of students listed.

### Sorting

1. **Click Column Headers**: Click on the column headers in any table to sort the data by that column.
2. **Ascending/Descending Order**: Click once to sort in ascending order and click again to sort in descending order. An arrow next to the column header indicates the current sort direction.

### Tooltips

1. **Hover Over Column Headers**: Hover your mouse over the column headers to see tooltips with additional information about each column. This helps you understand what each column represents.

## Code Structure

- `App.js`: Main component that handles the state and renders the other components.
- `components/`: Contains the UI components such as `Header`, `SearchBar`, `UniversityList`, `StudentData`, `ProgramSummary`, `SnapshotLinks`, and `ProgramIndex`.
- `utils/`: Contains utility functions for fetching and processing data.
- `App.css`: Contains the styles for the application.

## Data Flow

1. **Fetching Data**: Data is fetched from external sources using the `fetchVersions` and `fetchStudentData` functions.
2. **Processing Data**: The data is processed to compute program summaries and indexes using functions like `computeProgramSummary` and `computeProgramIndex`.
3. **State Management**: The state is managed using React hooks (`useState`, `useEffect`, `useRef`, `useCallback`).
4. **Rendering Components**: Based on the state, different components are rendered to display the data to the user.

## Key Functions

- **fetchData**: Fetches data based on the user's query.
- **handleSearchChange**: Updates the query state as the user types in the search bar.
- **handleStatistics**: Fetches and displays statistics for the selected program.
- **handleSort**: Sorts the data based on the selected column.

## Contributing

We welcome contributions from the community. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
