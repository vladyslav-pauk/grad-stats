import React, { useState, useEffect, useRef, useCallback } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Tabs, Tab } from 'react-bootstrap';
import debounce from 'lodash.debounce';
import logo from './ai-logo.svg';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import UniversityList from './components/UniversityList';
import StudentData from './components/StudentData';
import ProgramSummary from './components/ProgramSummary';
import SnapshotLinks from './components/SnapshotLinks';
import ProgramIndex from './components/ProgramIndex';
import StatisticsTab from './components/StatisticsTab'; // Import the new StatisticsTab component
import { fetchVersions, fetchStudentData } from './utils/dataFetch';
import { computeProgramSummary, computeProgramIndex } from './utils/dataProcess';
import { formatValue } from './utils/helpers';
// import { updateDatesAndCalculateAverage } from './utils/dataProcess';
import './App.css';

const App = () => {
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
    const searchInputRef = useRef(null);

    useEffect(() => {
        fetchVersions()
            .then(fetchStudentData)
            .then(data => {
                window.studentData = data;
            })
            .catch(error => console.error('Error fetching the JSON data:', error));
    }, []);

    const fetchData = useCallback((query) => {
        if (query && window.studentData) {
            const matches = window.studentData.filter(item =>
                item.University.toLowerCase().includes(query.toLowerCase())
            );
            const uniqueUniversities = Array.from(new Set(matches.map(item => item.University)));
            setUniversities(uniqueUniversities);
        } else {
            setUniversities([]);
        }
    }, []);

    useEffect(() => {
        const debouncedFetchData = debounce((q) => fetchData(q), 300);
        debouncedFetchData(query);
        return () => debouncedFetchData.cancel();
    }, [query, fetchData]);

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

    const handleEscapeKey = useCallback((event) => {
        if (event.key === 'Escape') {
            setUniversities([]);
            setHighlightIndex(-1);
            setHoverIndex(-1);
        }
    }, []);

    useEffect(() => {
        document.addEventListener('keydown', handleEscapeKey);
        return () => document.removeEventListener('keydown', handleEscapeKey);
    }, [handleEscapeKey]);

    useEffect(() => {
        if (searchInputRef.current) {
            searchInputRef.current.focus();
        }
    }, []);

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
        const filteredMatches = university ? window.studentData.filter(item => item.University.toLowerCase().includes(university.toLowerCase())) : window.studentData;

        setStats(filteredMatches);
        setProgramStatistics(computeProgramIndex(window.studentData));
        setStatistics(computeProgramSummary(filteredMatches));
        setCurrentProgram(university ? university : 'Overview');
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

            let aValue;
            let bValue;

            aValue = a[sortConfig.key];
            bValue = b[sortConfig.key];

            if ((sortConfig.key === 'enrollmentDate') || (sortConfig.key === 'completionDate')) {
                aValue = new Date(aValue.replace('< ', '').replace('> ', '')).getTime();
                bValue = new Date(bValue.replace('< ', '').replace('> ', '')).getTime();
            }

            if ((sortConfig.key === 'timeToDegree')) {
                aValue = parseFloat(aValue.replace('> ', ''));
                bValue = parseFloat(bValue.replace('> ', ''));
            }

            if (aValue < bValue) {
                return sortConfig.direction === 'ascending' ? -1 : 1;
            }
            if (aValue > bValue) {
                return sortConfig.direction === 'ascending' ? 1 : -1;
            }
            return 0;
        });
        return sortedData;
    };

    const renderTabs = () => (
        <Tabs activeKey={activeTab} onSelect={(k) => setActiveTab(k)} id="uncontrolled-tab-example" className="mt-3">
            {currentProgram !== 'Overview' && (
                <Tab eventKey="statistics" title="Summary">
                    <ProgramSummary statistics={statistics} />
                </Tab>
            )}
            {currentProgram === 'Overview' && (
                <Tab eventKey="programStatistics" title="Programs">
                    <ProgramIndex programs={programStatistics} onSelectProgram={handleStatistics} />
                </Tab>
            )}
            <Tab eventKey="data" title="Students">
                <StudentData
                    stats={sortedStats()}
                    sortConfig={sortConfig}
                    handleSort={handleSort}
                    formatValue={formatValue}
                    tableHoverIndex={tableHoverIndex}
                    setTableHoverIndex={setTableHoverIndex}
                    currentProgram={currentProgram}
                />
            </Tab>
            {currentProgram === 'Overview' && (
                <Tab eventKey="statisticsTab" title="Statistics">
                    <StatisticsTab programStatistics={programStatistics} />
                </Tab>
            )}
            {currentProgram !== 'Overview' && (
                <Tab eventKey="snapshots" title="Snapshots">
                    <SnapshotLinks stats={stats} />
                </Tab>
            )}
        </Tabs>
    );

    return (
        <div className="app-container">
            <div className="container">
                <Header />
                <SearchBar
                    query={query}
                    handleSearchChange={handleSearchChange}
                    handleSearchFocus={handleSearchFocus}
                    handleKeyDown={handleKeyDown}
                    logo={logo}
                    searchInputRef={searchInputRef}
                />
                {universities.length > 0 && (
                    <UniversityList
                        universities={universities}
                        dropdownRef={dropdownRef}
                        highlightIndex={highlightIndex}
                        hoverIndex={hoverIndex}
                        setHoverIndex={setHoverIndex}
                        handleStatistics={handleStatistics}
                        isDropdownHovered={isDropdownHovered}
                        setIsDropdownHovered={setIsDropdownHovered}
                    />
                )}
                {currentProgram && (
                    <div>
                        <h2>{currentProgram}</h2>
                        {renderTabs()}
                    </div>
                )}
                <footer className="app-footer">
                    <p className="app-footer-text">&copy; 2024 Grad Stats. All rights reserved.</p>
                </footer>
            </div>
        </div>
    );
};

export default App;
