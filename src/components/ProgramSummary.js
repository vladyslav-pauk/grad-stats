import React from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../App.css';
import { formatValue } from '../utils/helpers';

function ProgramSummary({ statistics }) {
    if (!statistics) return null;

    const {
        totalEntries,
        percentageOfPlacements,
        currentlyActive,
        earliestSnapshot,
        programLink,
        placementLink,
        numberOfSnapshots,
        averageDuration
    } = statistics;

    const placementRate = `${parseFloat(percentageOfPlacements).toFixed(0)}%`
    const programPage = <a href={programLink} target="_blank" rel="noopener noreferrer">{programLink}</a>
    const placementPage = <a href={placementLink} target="_blank" rel="noopener noreferrer">{placementLink}</a>

    const rows = [
        { label: 'Currently Enrolled', value: currentlyActive, tooltip: 'Number of students currently enrolled in the graduate program, according to the latest snapshot' },
        { label: 'Total Students Recorded', value: totalEntries, tooltip: 'Total number of students enrolled in the graduate program since the earliest record' },
        { label: 'Placement Rate', value: placementRate, tooltip: 'Percentage of students placed in jobs according to the placement page' },
        { label: 'Average Time-to-Degree', value: averageDuration, tooltip: 'Estimated mean time-to-degree, based on data from former students with known enrollment date' },
        { label: 'Number of Snapshots', value: numberOfSnapshots, tooltip: 'Total number of snapshots recorded for this program' },
        { label: 'Earliest Record', value: earliestSnapshot, tooltip: 'Earliest record of the graduate program in the web archive' },
        { label: 'Program Page', value: programPage, tooltip: 'Link to the program page' },
        { label: 'Placement Page', value: placementPage, tooltip: 'Link to the placement page' }
    ];

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                {/*<tbody>*/}
                {/*    {rows.map((row, index) => (*/}
                {/*        <OverlayTrigger*/}
                {/*            key={index}*/}
                {/*            placement="top"*/}
                {/*            overlay={<Tooltip id={`tooltip-${index}`}>{row.tooltip}</Tooltip>}*/}
                {/*        >*/}
                {/*            <tr key={index}>*/}
                {/*                <th>{row.label}</th>*/}
                {/*                <td>{formatValue(row.value, row, 'value')}</td>*/}
                {/*            </tr>*/}
                {/*        </OverlayTrigger>*/}
                {/*    ))}*/}
                {/*</tbody>*/}
                <tbody>
                {rows.map((row, index) => (
                    <tr key={index}>
                        <th>{row.label}</th>
                        <td>{formatValue(row.value, row, 'value')}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default ProgramSummary;