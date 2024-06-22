import React from 'react';
import { formatColumnName, formatValue } from '../utils/helpers';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../App.css';

const columnOrder = [
    'Name',
    'University',
    'Start_Date',
    'End_Date',
    'Years',
    'Active',
    'Placement',
    // Add other columns as needed
];

function DataTable({ stats, sortConfig, handleSort, tableHoverIndex, setTableHoverIndex, currentProgram }) {
    if (!stats) return null;

    const columns = columnOrder.filter(column => Object.keys(stats[0]).includes(column));

    const tooltipTexts = {
        University: 'The institution offering the program',
        Name: 'First and last name of the student',
        Active: 'Current enrollment status',
        Placement: 'Job placement status',
        Years: 'Duration of enrollment in years',
        Start_Date: 'Date when the student enrolled in the program',
        End_Date: 'Date when the student completed the program',
    };

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                    <tr>
                        <th>#</th>
                        {columns.map((column) => (
                            (currentProgram === 'All Programs' || column !== 'University') && (
                                <OverlayTrigger
                                    key={column}
                                    placement="top"
                                    overlay={
                                        <Tooltip id={`tooltip-${column}`}>
                                            {tooltipTexts[column] || `Info about ${formatColumnName(column)}`}
                                        </Tooltip>
                                    }
                                >
                                    <th
                                        onClick={() => handleSort(column)}
                                        className={`sortable ${sortConfig.key === column && sortConfig.direction ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}
                                    >
                                        {formatColumnName(column)}
                                    </th>
                                </OverlayTrigger>
                            )
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {stats.map((row, rowIndex) => (
                        <tr
                            key={rowIndex}
                            className={rowIndex === tableHoverIndex ? 'table-active' : ''}
                            onMouseEnter={() => setTableHoverIndex(rowIndex)}
                            onMouseLeave={() => setTableHoverIndex(-1)}
                        >
                            <td>{rowIndex + 1}</td>
                            {columns.map((column) => (
                                (currentProgram === 'All Programs' || column !== 'University') && (
                                    <td key={column}>{formatValue(row[column], row, column)}</td>
                                )
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataTable;