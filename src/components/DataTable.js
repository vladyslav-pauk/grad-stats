import React from 'react';
import { formatColumnName, formatValue } from '../utils/helpers';
import '../App.css';

function DataTable({ stats, sortConfig, handleSort, tableHoverIndex, setTableHoverIndex, currentProgram }) {
    if (!stats) return null;

    const columns = Object.keys(stats[0]).filter(column => column !== 'Snapshots');

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                    <tr>
                        <th>#</th>
                        {columns.map((column) => (
                            (currentProgram === 'All Programs' || column !== 'University') && (
                                <th
                                    key={column}
                                    onClick={() => handleSort(column)}
                                    className={`sortable ${sortConfig.key === column && sortConfig.direction ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}
                                >
                                    {formatColumnName(column)}
                                </th>
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