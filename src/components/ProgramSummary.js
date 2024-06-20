import React from 'react';
import '../App.css';

function SummaryStatistics({ statistics }) {
    if (!statistics) return null;

    const { totalEntries, percentageOfPlacements, currentlyActive, earliestSnapshot, programLink, placementLink, numberOfSnapshots, ...otherStats } = statistics;

    const formatColumnName = (column) => {
        if (column === 'Years') return 'Average Duration';
        return column.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    };

    const rows = [
        { label: 'Currently Enrolled', value: currentlyActive },
        { label: 'Total Students', value: totalEntries },
        { label: 'Placement Rate', value: `${parseFloat(percentageOfPlacements).toFixed(0)}%` },
        ...Object.keys(otherStats).map(key => ({
            label: formatColumnName(key),
            value: otherStats[key].toFixed ? otherStats[key].toFixed(1) : otherStats[key]
        })),
        { label: 'Number of Snapshots', value: numberOfSnapshots },
        { label: 'Earliest Record', value: earliestSnapshot },
        { label: 'Program Page', value: <a href={programLink} target="_blank" rel="noopener noreferrer">{programLink}</a> },
        { label: 'Placement Page', value: <a href={placementLink} target="_blank" rel="noopener noreferrer">{placementLink}</a> }
    ];

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <tbody>
                    {rows.map((row, index) => (
                        <tr key={index}>
                            <th>{row.label}</th>
                            <td>{row.value}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default SummaryStatistics;