import React from 'react';
import '../App.css';

function ProgramSummary({ statistics }) {
    if (!statistics) return null;

    const {
        totalEntries,
        percentageOfPlacements,
        currentlyActive,
        originalStartDate,
        programLink,
        placementLink,
        numberOfSnapshots,
        averageDuration
    } = statistics;

    // const formatColumnName = (column) => {
    //     if (column === 'Years') return 'Average Duration';
    //     // return column.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    //     return column
    // };

    const placementRate = `${parseFloat(percentageOfPlacements).toFixed(0)}%`
    const programPage = <a href={programLink} target="_blank" rel="noopener noreferrer">{programLink}</a>
    const placementPage = <a href={placementLink} target="_blank" rel="noopener noreferrer">{placementLink}</a>

    const rows = [
        {label: 'Currently Enrolled', value: currentlyActive},
        {label: 'Total Students Recorded', value: totalEntries},
        {label: 'Placement Rate', value: placementRate},
        {label: 'Average Time-to-Degree', value: averageDuration},
        {label: 'Number of Snapshots', value: numberOfSnapshots},
        {label: 'Earliest Record', value: originalStartDate},
        {label: 'Program Page', value: programPage},
        {label: 'Placement Page', value: placementPage}
        // ...Object.keys(otherStats).map(key => ({
        //     label: formatColumnName(key),
        //     value: otherStats[key].toFixed ? otherStats[key].toFixed(1) : otherStats[key]
        // })),
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

export default ProgramSummary;