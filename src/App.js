import React, { useState, useEffect, useRef } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Tabs, Tab } from 'react-bootstrap';
import debounce from 'lodash.debounce';
import logo from './ai-logo.svg';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import UniversityList from './components/UniversityList';
import DataTable from './components/DataTable'; // Updated to import DataTable
import SummaryStatistics from './components/SummaryStatistics';
import SnapshotLinks from './components/SnapshotLinks';
import ProgramStatistics from './components/ProgramStatistics';
import { fetchVersions, fetchStudentData } from './utils/dataFetch';
import { formatValue, computeStatistics, computeStatisticsForPrograms } from './utils/helpers';
import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [universities, setUniversities] = useState([]);
    const [stats, setStats] = useState([]);
    const [statistics, setStatistics] = useState({});
    const [programStatistics, setProgramStatistics] = useState([]);
    const [currentProgram, setCurrentProgram] = useState('');
    const [activeTab, setActiveTab] = useState('programStatistics');
    const [highlightIndex, setHighlightIndex] = useState(-1);
    const [hoverIndex, setHoverIndex] = useState(-1);
    const [tableHoverIndex, setTableHoverIndex] = useState(-1);
    const [isDropdownHovered, setIsDropdownHovered] = useState(false);
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });
    const dropdownRef = useRef(null);

    useEffect(() => {
        fetchVersions().then(fetchStudentData).then(data => {
            window.studentData = data;
            setProgramStatistics(computeStatisticsForPrograms(data)); // Set initial program statistics
        }).catch(error => console.error('Error fetching the JSON data:', error));
    }, []);

    const fetchData = (query) => {
        if (query && window.studentData) {
            const matches = window.studentData.filter(item =>
                item.University.toLowerCase().includes(query.toLowerCase())
            );
            const uniqueUniversities = Array.from(new Set(matches.map(item => item.University)));
            setUniversities(uniqueUniversities);
        } else {
            setUniversities([]);
        }
    };

    const debouncedFetchData = debounce(fetchData, 300);

    useEffect(() => {
        debouncedFetchData(query);
        return () => debouncedFetchData.cancel();
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
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [dropdownRef]);

    const fetchAllPrograms = () => {
        if (window.studentData) {
            const uniqueUniversities = Array.from(new Set(window.studentData.map(item => item.University)));
            setUniversities(uniqueUniversities);
        }
    };

    const handleSearchChange = (event) => {
        setQuery(event.target.value);
        setHighlightIndex(-1);
    };

    const handleSearchFocus = () => {
        if (query === '') {
            fetchAllPrograms();
        }
    };

    const handleStatistics = (university = '') => {
        if (!window.studentData) return;
        const matches = university ? window.studentData.filter(item => item.University.toLowerCase().includes(university.toLowerCase())) : window.studentData;
        const filteredMatches = matches.map(({ URL, Snapshots, Department, ...rest }) => {
            Object.keys(rest).forEach(key => {
                if (key.toLowerCase().includes('date') || key.toLowerCase().includes('time')) {
                    rest[key] = new Date(rest[key]).toLocaleDateString();
                }
            });
            return { ...rest, Snapshots }; // Ensure Snapshots field is retained
        });

        setStats(filteredMatches);
        setStatistics(computeStatistics(filteredMatches));
        setProgramStatistics(computeStatisticsForPrograms(window.studentData));
        setCurrentProgram(university ? university : 'All Programs');
        setActiveTab(university ? 'statistics' : 'programStatistics');
        setUniversities([]);
        setQuery('');
        setHighlightIndex(-1);
        setTableHoverIndex(-1);
        setHoverIndex(-1);
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

    const handleSort = (column) => {
        let direction = 'ascending';
        if (sortConfig.key === column && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key: column, direction });
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

    const renderTabs = () => {
        return (
            <Tabs activeKey={activeTab} onSelect={(k) => setActiveTab(k)} id="uncontrolled-tab-example" className="mt-3">
                {currentProgram !== 'All Programs' && (
                    <Tab eventKey="statistics" title="Summary">
                        <SummaryStatistics statistics={statistics} />
                    </Tab>
                )}
                {currentProgram === 'All Programs' && (
                    <Tab eventKey="programStatistics" title="Programs">
                        <ProgramStatistics programs={programStatistics} onSelectProgram={handleStatistics} />
                    </Tab>
                )}
                <Tab eventKey="data" title="Data">
                    <DataTable stats={sortedStats()} sortConfig={sortConfig} handleSort={handleSort} formatValue={formatValue} tableHoverIndex={tableHoverIndex} setTableHoverIndex={setTableHoverIndex} currentProgram={currentProgram} />
                </Tab>
                {currentProgram !== 'All Programs' && (
                    <Tab eventKey="snapshots" title="Snapshots">
                        <SnapshotLinks stats={stats} />
                    </Tab>
                )}
            </Tabs>
        );
    };

    return (
        <div className="app-container">
            <div className="container">
                <Header />
                <SearchBar query={query} handleSearchChange={handleSearchChange} handleSearchFocus={handleSearchFocus} handleKeyDown={handleKeyDown} logo={logo} />
                {universities.length > 0 && <UniversityList universities={universities} dropdownRef={dropdownRef} highlightIndex={highlightIndex} hoverIndex={hoverIndex} setHoverIndex={setHoverIndex} handleStatistics={handleStatistics} isDropdownHovered={isDropdownHovered} setIsDropdownHovered={setIsDropdownHovered} />}
                {currentProgram && (
                    <div>
                        <h2>{currentProgram}</h2>
                        {renderTabs()}
                    </div>
                )}
                <footer className="app-footer">
                    <p className="app-footer-text">&copy; 2024 PhD Stats. All rights reserved.</p>
                </footer>
            </div>
        </div>
    );
}

export default App;
