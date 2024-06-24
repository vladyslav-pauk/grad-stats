import React from 'react';
import { formatColumnName, formatValue } from '../utils/helpers';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../App.css';

const columnOrder = [
    'Name',
    'University',
    'enrollmentDate',
    'completionDate',
    'timeToDegree',
    'Active',
    'Placement',
];

function StudentData({ stats, sortConfig, handleSort, tableHoverIndex, setTableHoverIndex, currentProgram }) {
    if (!stats) return null;

    const columns = columnOrder
    .filter(column => Object.keys(stats[0]).includes(column))
    .filter(column => currentProgram === 'Program Index' || (column !== 'University'))
    // .filter(column => currentProgram !== 'Program Index' || (column !== 'Start_Date' && column !== 'End_Date'))
    ;

    const tooltipTexts = {
        University: 'The institution offering the program',
        Name: 'First and last name of the student',
        Active: 'Current enrollment status according to the latest snapshot',
        Placement: 'Job placement status according to the placement page',
        timeToDegree: 'Estimated time-to-degree in years',
        enrollmentDate: 'Estimated enrollment date',
        completionDate: 'Estimated completion date',
    };

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                    <tr>
                        <th>#</th>
                        {columns.map((column) => (
                            <OverlayTrigger
                                key={column}
                                placement="top"
                                overlay={
                                    <Tooltip id={`tooltip-${column}`}>
                                        {tooltipTexts[column]}
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
                                <td key={column}>{formatValue(row[column], row, column)}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default StudentData;