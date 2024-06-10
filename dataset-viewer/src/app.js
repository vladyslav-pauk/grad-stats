import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import debounce from 'lodash.debounce';
import logo from './ai-logo.png'; // Make sure to add the logo image to your src directory

function App() {
    const [query, setQuery] = useState('');
    const [universities, setUniversities] = useState([]);
    const [stats, setStats] = useState(null);
    const [currentProgram, setCurrentProgram] = useState('');
    const [highlightIndex, setHighlightIndex] = useState(-1);
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });

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
            <div className="mt-3">
                <h2>{currentProgram}</h2>
                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th>#</th>
                        {columns.map((column) => (
                            <th key={column} onClick={() => handleSort(column)} style={{cursor: 'pointer'}}>
                                {column} {sortConfig.key === column ? (sortConfig.direction === 'ascending' ? '▲' : '▼') : ''}
                            </th>
                        ))}
                    </tr>
                    </thead>
                    <tbody>
                    {sortedData.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            <td>{rowIndex + 1}</td>
                            {columns.map((column) => (
                                <td key={column}>{formatValue(row[column])}</td>
                            ))}
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="container">
            <p></p>
            <h1 className="text-center">PhD Stats</h1>
            <p className="text-center">Powered by AI &nbsp; <img src={logo} alt="Powered by AI"
                                                                 style={{height: '20px'}}/></p>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Search for a university"
                    value={query}
                    onChange={handleSearchChange}
                    onKeyDown={handleKeyDown}
                />
            </div>
            {universities.length > 0 && (
                <ul className="list-group">
                    {universities.map((university, index) => (
                        <li
                            key={index}
                            className={`list-group-item ${index === highlightIndex ? 'active' : ''}`}
                            onClick={() => handleStatistics(university)}
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
    );
}

export default App;