import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import background from './background-image.jpg';
import debounce from 'lodash.debounce';
import logo from './ai-logo.png'; // Make sure to add the logo image to your src directory

function App() {
    const [query, setQuery] = useState('');
    const [universities, setUniversities] = useState([]);
    const [stats, setStats] = useState(null);
    const [currentProgram, setCurrentProgram] = useState('');
    const [highlightIndex, setHighlightIndex] = useState(-1);
    const [hoverIndex, setHoverIndex] = useState(-1);
    const [tableHoverIndex, setTableHoverIndex] = useState(-1);
    const [isDropdownHovered, setIsDropdownHovered] = useState(false);
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });
    const dropdownRef = useRef(null); // Add this line

    useEffect(() => {
        const fetchData = async () => {
            if (query) {
                try {
                    const response = await axios.get(`http://127.0.0.1:5000/search?query=${query}`);
                    setUniversities(response.data);
                } catch (error) {
                    console.error("There was an error fetching the data!", error);
                }
            } else {
                setUniversities([]);
            }
        };

        const debouncedFetchData = debounce(fetchData, 300);
        debouncedFetchData();

        // Cleanup function to cancel debounced call if query changes before debounce delay
        return () => {
            debouncedFetchData.cancel();
        };
    }, [query]);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setUniversities([]);
                setHighlightIndex(-1);
                setHoverIndex(-1);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [dropdownRef]);

    const fetchAllPrograms = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/search?query=`);
            setUniversities(response.data);
        } catch (error) {
            console.error("There was an error fetching the data!", error);
        }
    };

    const handleSearchChange = (event) => {
        setQuery(event.target.value);
        setHighlightIndex(-1); // Reset highlight index when query changes
    };

    const handleStatistics = async (university = '') => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/statistics?query=${university}`);
            setStats(response.data);
            setCurrentProgram(university ? `${university}` : 'All Programs');
            setUniversities([]); // Clear the search results
            setQuery(''); // Clear the search query
            setHighlightIndex(-1); // Reset highlight index
        } catch (error) {
            console.error("There was an error fetching the data!", error);
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
            if (universities.length === 0 && query === '') {
                fetchAllPrograms();
            } else {
                if (event.key === 'ArrowDown') {
                    setHighlightIndex((prevIndex) => (prevIndex + 1) % universities.length);
                } else if (event.key === 'ArrowUp') {
                    setHighlightIndex((prevIndex) => (prevIndex + universities.length - 1) % universities.length);
                }
            }
        } else if (event.key === 'Enter') {
            if (highlightIndex >= 0) {
                handleStatistics(universities[highlightIndex]);
            } else if (query === '') {
                handleStatistics();
            }
        }
    };

    const formatValue = (value) => {
        if (typeof value === 'boolean') {
            return value ? 'Yes' : 'No';
        }
        if (typeof value === 'number') {
            return value.toFixed(1);
        }
        const date = new Date(value);
        if (!isNaN(date)) {
            return date.toLocaleDateString();
        }
        return String(value);
    };

    const handleSort = (column) => {
        let direction = 'ascending';
        if (sortConfig.key === column && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key: column, direction: direction });
    };

    const sortedStats = () => {
        if (!stats || !sortConfig.key) {
            return stats;
        }
        const sortedData = [...stats];
        sortedData.sort((a, b) => {
            if (a[sortConfig.key] < b[sortConfig.key]) {
                return sortConfig.direction === 'ascending' ? -1 : 1;
            }
            if (a[sortConfig.key] > b[sortConfig.key]) {
                return sortConfig.direction === 'ascending' ? 1 : -1;
            }
            return 0;
        });
        return sortedData;
    };

    const renderStatistics = (stats) => {
        if (!stats) return null;

        const sortedData = sortedStats();
        const columns = Object.keys(sortedData[0]);

        return (
            <div
                className="mt-3"
            >
                <h2>{currentProgram}</h2>
                <table className="table table-striped table">
                    <thead>
                    <tr>
                        <th>#</th>
                        {columns.map((column) => (
    (currentProgram === 'All Programs' || column !== 'University') && (
        <th key={column} onClick={() => handleSort(column)} style={{ cursor: 'pointer' }}>
            {column} {sortConfig.key === column ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
        </th>
    )
))}
                    </tr>
                    </thead>
                    <tbody>
                    {sortedData.map((row, rowIndex) => (
                        <tr
                            key={rowIndex}
                            className={rowIndex === highlightIndex || (rowIndex === tableHoverIndex && !isDropdownHovered) ? 'table-active' : ''}
                            onMouseEnter={() => setTableHoverIndex(rowIndex)}
                            onMouseLeave={() => setTableHoverIndex(-1)}
                        >
                            <td>{rowIndex + 1}</td>
                            {columns.map((column) => (
    (currentProgram === 'All Programs' || column !== 'University') && (
        <td key={column}>{formatValue(row[column])}</td>
    )
))}
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div
            style={{
                fontFamily: "Merriweather, Georgia, serif",
                backgroundImage: `url(${background})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                minHeight: '100vh',
                margin: 0,
                // add bottom margin to footer
                padding: 20,
                // display: 'flex',
                // flexDirection: 'column',
                // justifyContent: 'center',
                // alignItems: 'center',
                // color: 'black'
            }}
        >

            <div
                className="container"
            >
                <div style={{height: '10px'}}></div>
                <h1 className="text-center">PhD Stats</h1>
                <div style={{height: '10px'}}></div>
                <div className="form-group">
                    <label
                        style={{
                            display: 'block',
                            position: 'relative'
                            }}
                    >
                        <input
                            type="text"
                            name="notASearchField"
                            className="form-control"
                            placeholder="Enter program name or press enter for all programs"
                            value={query}
                            onChange={handleSearchChange}
                            onKeyDown={handleKeyDown}
                            // autoComplete="off" // Changed this line
                            // autoCorrect="off" // Add this line
                            // autoCapitalize="off" // Add this line
                            // spellCheck="false"
                        />
                    </label>
                        <span className="powered-by-ai"
                              style={{
                                  display: 'block',
                                  textAlign: 'right',
                                  fontSize: '12px',
                                  marginTop: '10px'
                              }}
                        >
                        Powered by GPT &nbsp;
                            <img
                                src={logo}
                                alt="Powered by AI"
                                style={{height: '15px', verticalAlign: 'top'}}
                            />
                    </span>
                </div>
                {universities.length > 0 && (
                    <ul
                        className="list-group"
                        ref={dropdownRef}
                        onMouseEnter={() => setIsDropdownHovered(true)}
                        onMouseLeave={() => setIsDropdownHovered(false)}
                    >
                        {universities.map((university, index) => (
                            <li
                                key={index}
                                className={`list-group-item ${index === (highlightIndex >= 0 && hoverIndex === -1 ? highlightIndex : hoverIndex) ? 'active' : ''}`}
                                onClick={() => handleStatistics(university)}
                                onMouseEnter={() => setHoverIndex(index)}
                                onMouseLeave={() => setHoverIndex(-1)}
                                style={{cursor: 'pointer'}}
                            >
                                {university}
                            </li>
                        ))}
                    </ul>
                )}
                {renderStatistics(stats)}
                <footer className="mt-5">
                    <p className="text-center">&copy; 2024 PhD Stats. All rights reserved.</p>
                </footer>
            </div>
        </div>
);
}

export default App;