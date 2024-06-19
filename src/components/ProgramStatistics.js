import React, { useState } from 'react';
import '../App.css';

function ProgramStatistics({ programs, onSelectProgram }) {
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });
    const [hoverIndex, setHoverIndex] = useState(-1);

    const formatColumnName = (column) => {
        if (column === 'totalEntries') return 'Total Students';
        if (column === 'currentlyActive') return 'Currently Enrolled';
        if (column === 'percentageOfPlacements') return 'Placement Rate';
        if (column === 'Average Duration') return 'Average Duration';
        if (column === 'earliestSnapshot') return 'Earliest Record';
        return column.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    };

    const columns = ['Program', 'currentlyActive', 'totalEntries', 'percentageOfPlacements', 'Average Duration', 'earliestSnapshot'];

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const sortedPrograms = [...programs].sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
            return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
            return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
    });

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                    <tr>
                        <th>#&emsp;</th>
                        {columns.map((column) => (
                            <th
                                key={column}
                                onClick={() => requestSort(column)}
                                className={`sortable ${sortConfig.key === column ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}
                            >
                                {formatColumnName(column)}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {sortedPrograms.map((program, rowIndex) => (
                        <tr
                            key={rowIndex}
                            className={rowIndex === hoverIndex ? 'table-active' : ''}
                            onMouseEnter={() => setHoverIndex(rowIndex)}
                            onMouseLeave={() => setHoverIndex(-1)}
                            onClick={() => onSelectProgram(program.Program)}
                            style={{ cursor: 'pointer' }}
                        >
                            <td>{rowIndex + 1}</td>
                            {columns.map((column) => (
                                <td key={column}>
                                    {column === 'percentageOfPlacements'
                                        ? `${parseFloat(program[column]).toFixed(0)}%`
                                        : column === 'totalEntries' || column === 'currentlyActive' || column === 'percentageOfPlacements'
                                        ? program[column]
                                        : column === 'earliestSnapshot' && program[column] === 'N/A'
                                        ? 'N/A'
                                        : program[column].toFixed
                                        ? program[column].toFixed(1)
                                        : program[column]
                                    }
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ProgramStatistics;