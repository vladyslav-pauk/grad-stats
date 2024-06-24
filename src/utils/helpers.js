export const extractDateFromUrl = (url) => {
    const match = url.match(/web\/(\d{14})/);
    if (match) {
        const dateStr = match[1];
        const year = dateStr.slice(0, 4);
        const month = dateStr.slice(4, 6);
        const day = dateStr.slice(6, 8);
        return { date: new Date(year, month - 1, day), formattedDate: `${month}/${day}/${year}` };
    }
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString();
    return { date: currentDate, formattedDate };
};

export const formatValue = (value, row, column) => {
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    if (value === '0.00') {
        return 'N/A';
    }
    if (column === 'percentageOfPlacements') {
        return `${parseFloat(value).toFixed(0)}%`;
    }
    if (typeof value === 'number') {
        return value.toFixed(0);
    }
    if (value === '> 0.00') {
        return 'N/A';
    }
    return value;
};

export const formatColumnName = (column) => {
    if (column === 'timeToDegree') return 'Time-to-Degree';
    if (column === 'enrollmentDate') return 'Enrollment Date';
    if (column === 'completionDate') return 'Completion Date';
    if (column === 'Active') return 'Enrolled';
    if (column === 'University') return 'Host Institution';
    if (column === 'program') return 'Host Institution';
    if (column === 'totalEntries') return 'Total Students';
    if (column === 'currentlyActive') return 'Currently Enrolled';
    if (column === 'percentageOfPlacements') return 'Placement Rate';
    if (column === 'averageDuration') return 'Time-to-Degree';
    if (column === 'earliestSnapshot') return 'Earliest Record';
    return column.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};