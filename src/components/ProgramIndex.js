import React, { useState } from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import { formatColumnName, formatValue } from '../utils/helpers';
import '../App.css';

function ProgramIndex({ programs, onSelectProgram }) {
    const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });
    const [hoverIndex, setHoverIndex] = useState(-1);

    const columns = ['program', 'currentlyActive', 'totalEntries', 'earliestSnapshot', 'averageDuration', 'percentageOfPlacements'];

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const sortedPrograms = [...programs].sort((a, b) => {
        let aValue = a[sortConfig.key];
        let bValue = b[sortConfig.key];

        if (sortConfig.key === 'percentageOfPlacements') {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        } else if (sortConfig.key === 'earliestSnapshot') {
            aValue = new Date(aValue);
            bValue = new Date(bValue);
        }

        if (aValue < bValue) {
            return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (aValue > bValue) {
            return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
    });

    const tooltipTexts = {
        program: 'The institution offering the program',
        currentlyActive: 'Number of students currently enrolled in the graduate program, according to the latest snapshot',
        totalEntries: 'Total number of students enrolled in the graduate program since the earliest record',
        percentageOfPlacements: 'Percentage of students placed in jobs according to the placement page',
        averageDuration: 'Estimated mean time-to-degree, based on data from former students with known enrollment date',
        earliestSnapshot: 'Earliest record of the graduate program in the web archive',
    };

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                    <tr>
                        <th>#&emsp;</th>
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
                                    onClick={() => requestSort(column)}
                                    className={`sortable ${sortConfig.key === column ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}
                                >
                                    {formatColumnName(column)}
                                </th>
                            </OverlayTrigger>
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
                            onClick={() => onSelectProgram(program.program)}
                            style={{ cursor: 'pointer' }}
                        >
                            <td>{rowIndex + 1}</td>
                            {columns.map((column) => (
                                <td key={column}>
                                    {formatValue(program[column], program, column)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ProgramIndex;