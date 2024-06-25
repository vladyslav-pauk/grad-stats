import React, { useState } from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import { extractDateFromUrl } from "../utils/helpers";
import '../App.css';

function SnapshotLinks({ stats }) {
    const [sortConfig, setSortConfig] = useState({ key: 'date', direction: '' });

    if (!stats) return null;

    const snapshotMap = new Map();

    stats.forEach(entry => {
        if (entry.Snapshots && entry.Snapshots.length > 0) {
            entry.Snapshots.forEach(snapshot => {
                const { date, formattedDate } = extractDateFromUrl(snapshot);
                if (!snapshotMap.has(formattedDate)) {
                    snapshotMap.set(formattedDate, { date, formattedDate, url: snapshot, count: 0 });
                }
                const currentEntry = snapshotMap.get(formattedDate);
                snapshotMap.set(formattedDate, { date, formattedDate, url: snapshot, count: currentEntry.count + 1 });
            });
        }
    });

    const sortedSnapshots = Array.from(snapshotMap.values()).sort((a, b) => {
        if (sortConfig.key === 'date') {
            return sortConfig.direction === 'ascending' ? a.date - b.date : b.date - a.date;
        } else if (sortConfig.key === 'count') {
            return sortConfig.direction === 'ascending' ? a.count - b.count : b.count - a.count;
        }
        return 0;
    });

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const tooltipTexts = {
        date: 'Date when the snapshot was taken',
        count: 'Number of students listed in the snapshot',
        // link: 'Snapshot URL'
    };

    return (
        <div className="mt-3">
            <table className="table table-striped table-transparent">
                <thead>
                <tr>
                    <th>#</th>
                    <OverlayTrigger
                        key="date"
                        placement="top"
                        overlay={<Tooltip id="tooltip-date">{tooltipTexts.date}</Tooltip>}
                    >
                        <th onClick={() => requestSort('date')}
                            className={`sortable ${sortConfig.key === 'date' && sortConfig.direction ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}>
                            Date
                        </th>
                    </OverlayTrigger>
                    <OverlayTrigger
                        key="count"
                        placement="top"
                        overlay={<Tooltip id="tooltip-count">{tooltipTexts.count}</Tooltip>}
                    >
                        <th onClick={() => requestSort('count')}
                            className={`sortable ${sortConfig.key === 'count' && sortConfig.direction ? (sortConfig.direction === 'ascending' ? 'ascending' : 'descending') : ''}`}>
                            Students
                        </th>
                    </OverlayTrigger>
                    <th>Link</th>
                    {/*<OverlayTrigger*/}
                    {/*    key="link"*/}
                    {/*    placement="top"*/}
                    {/*    overlay={<Tooltip id="tooltip-link">{tooltipTexts.link}</Tooltip>}*/}
                    {/*>*/}
                    {/*    <th>Link</th>*/}
                    {/*</OverlayTrigger>*/}
                </tr>
                </thead>
                <tbody>
                    {sortedSnapshots.map(({ formattedDate, url, count }, idx) => (
                        <tr key={idx}>
                            <td style={{whiteSpace: 'nowrap'}}>
                                {idx + 1}
                                <span style={{display: 'inline-block', width: '13px'}}></span>
                            </td>
                            <td>{formattedDate}</td>
                            <td>{count}</td>
                            <td><a href={url} target="_blank" rel="noopener noreferrer">{url}</a></td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {sortedSnapshots.length === 0 && <p>No snapshot links available.</p>}
        </div>
    );
}

export default SnapshotLinks;