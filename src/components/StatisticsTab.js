import React, { useState, useMemo } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import { Row, Col, DropdownButton, Dropdown } from 'react-bootstrap';

const StatisticsTab = ({ programStatistics }) => {
    const [selectedMetric, setSelectedMetric] = useState('Placement Rate');

    const getFilteredData = () => {
        if (selectedMetric === 'Placement Rate') {
            return programStatistics.filter(item => item.percentageOfPlacements !== '0.00' && item.percentageOfPlacements !== 'N/A');
        } else {
            return programStatistics.filter(item => item.averageDuration !== '0.00' && item.averageDuration !== 'N/A');
        }
    };

    const filteredData = useMemo(getFilteredData, [selectedMetric, programStatistics]);

    const sortedData = useMemo(() => {
        return selectedMetric === 'Placement Rate'
            ? filteredData.sort((a, b) => b.percentageOfPlacements - a.percentageOfPlacements)
            : filteredData.sort((a, b) => b.averageDuration - a.averageDuration);
    }, [filteredData, selectedMetric]);

    const chartData = useMemo(() => {
        return {
            labels: sortedData.map(item => item.program),
            datasets: [
                {
                    label: selectedMetric,
                    data: selectedMetric === 'Placement Rate'
                        ? sortedData.map(item => item.percentageOfPlacements)
                        : sortedData.map(item => item.averageDuration),
                    backgroundColor: 'rgba(30, 150, 162, 0.9)',
                    borderColor: 'rgba(30, 150, 162, 1)',
                    borderWidth: 1,
                },
            ],
        };
    }, [sortedData, selectedMetric]);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
            },
        },
        layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
            },
        },
        plugins: {
            legend: {
                display: false,
            },
        },
    };

    const calculateStatistics = (data, key) => {
    const values = data.map(item => parseFloat(item[key])).filter(val => !isNaN(val));
    const totalPrograms = values.length;
    const mean = (values.reduce((acc, val) => acc + val, 0) / totalPrograms).toFixed(2);
    const std = (Math.sqrt(values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / totalPrograms)).toFixed(2);
    const min = Math.min(...values).toFixed(2);
    const max = Math.max(...values).toFixed(2);
    const median = values.sort((a, b) => a - b)[Math.floor(totalPrograms / 2)].toFixed(2);

    return { median, mean, std, min, max, totalPrograms };
};

const statistics = useMemo(() => {
    const stats = selectedMetric === 'Placement Rate'
        ? calculateStatistics(sortedData, 'percentageOfPlacements')
        : calculateStatistics(sortedData, 'averageDuration');

    if (selectedMetric === 'Placement Rate') {
        stats.mean += '%';
        stats.median += '%';
        stats.std += '%';
        stats.min += '%';
        stats.max += '%';
    }

    return stats;
}, [sortedData, selectedMetric]);

    return (
    <div>
        {/*<h3>Statistics</h3>*/}
        <Row noGutters>
            <Col md={4} className="stat-summary d-flex flex-column justify-content-center align-items-center">
                <DropdownButton
                    id="dropdown-basic-button"
                    title={selectedMetric}
                    className="mb-3 custom-dropdown"
                >
                    <Dropdown.Item onClick={() => setSelectedMetric('Placement Rate')}>Placement Rate</Dropdown.Item>
                    <Dropdown.Item onClick={() => setSelectedMetric('Time to Degree')}>Time to Degree</Dropdown.Item>
                </DropdownButton>
                <div>
                    <h4> </h4>
                    <ul>
                        <li><span className="stat-label">Mean:</span><span
                            className="stat-value">{statistics.mean}</span></li>
                        <li><span className="stat-label">Median:</span><span
                            className="stat-value">{statistics.median}</span></li>
                        <li><span className="stat-label">Standard Deviation:</span><span
                            className="stat-value">{statistics.std}</span></li>
                        <li><span className="stat-label">Min:</span><span className="stat-value">{statistics.min}</span>
                        </li>
                        <li><span className="stat-label">Max:</span><span className="stat-value">{statistics.max}</span>
                        </li>
                        <li><span className="stat-label">Total Programs:</span><span
                            className="stat-value">{statistics.totalPrograms}</span></li>
                    </ul>
                </div>
            </Col>
            <Col md={8}>
                <div className="chart-container">
                <Bar data={chartData} options={options} />
                </div>
            </Col>
        </Row>
    </div>
);
};

export default StatisticsTab;