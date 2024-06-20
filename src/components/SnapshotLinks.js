import React, { useState } from 'react';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../App.css';

function SnapshotLinks({ stats }) {
    const [sortConfig, setSortConfig] = useState({ key: 'date', direction: '' });

    if (!stats) return null;

    const extractDateFromUrl = (url) => {
        const match = url.match(/web\/(\d{14})/);
        if (match) {
            const dateStr = match[1];
            const year = dateStr.slice(0, 4);
            const month = dateStr.slice(4, 6);
            const day = dateStr.slice(6, 8);
            return { date: new Date(year, month - 1, day), formattedDate: `${month}/${day}/${year}` };
        }
        // For non-archived URLs, use the current date
        const currentDate = new Date();
        const formattedDate = currentDate.toLocaleDateString();
        return { date: currentDate, formattedDate };
    };

    const snapshotMap = new Map();

    stats.forEach(entry => {
        if (entry.Snapshots && entry.Snapshots.length > 0) {
            entry.Snapshots.forEach(snapshot => {
                const { date, formattedDate } = extractDateFromUrl(snapshot);
                if (!snapshotMap.has(formattedDate)) {
                    snapshotMap.set(formattedDate, { date, formattedDate, url: snapshot, count: 0 });
                }
                snapshotMap.get(formattedDate).count += 1;
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
        count: 'Number of students associated with the snapshot',
        link: 'Link to the snapshot'
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
                    <OverlayTrigger
                        key="link"
                        placement="top"
                        overlay={<Tooltip id="tooltip-link">{tooltipTexts.link}</Tooltip>}
                    >
                        <th>Link</th>
                    </OverlayTrigger>
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