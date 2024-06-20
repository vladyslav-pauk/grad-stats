export const formatValue = (value, row, column) => {
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    if (typeof value === 'number') {
        return value.toFixed(1);
    }
    if (column === 'End_Date' && row && row.Active) {
        return 'N/A';
    }
    const date = new Date(value);
    if (!isNaN(date)) {
        return date.toLocaleDateString();
    }
    return String(value);
};

export const computeStatisticsForPrograms = (data) => {
    const programs = {};

    data.forEach((entry) => {
        const program = entry.University;
        if (!programs[program]) {
            programs[program] = {
                totalEntries: 0,
                placedStudents: 0,
                currentlyActive: 0,
                totalYears: 0,
                yearsCount: 0,
                earliestSnapshot: null
            };
        }

        programs[program].totalEntries += 1;
        if (entry.Placement === true) {
            programs[program].placedStudents += 1;
        }

        if (entry.Active === true) {
            programs[program].currentlyActive += 1;
        }

        if (entry.Years && !entry.Active) {
            programs[program].totalYears += entry.Years;
            programs[program].yearsCount += 1;
        }

        if (entry.Start_Date) {
            const startDate = new Date(entry.Start_Date);
            if (!programs[program].earliestSnapshot || startDate < programs[program].earliestSnapshot) {
                programs[program].earliestSnapshot = startDate;
            }
        }
    });

    return Object.keys(programs).map(program => {
        const stats = programs[program];
        const averageDuration = stats.yearsCount > 0 ? (stats.totalYears / stats.yearsCount).toFixed(2) : 'N/A';
        return {
            Program: program,
            totalEntries: stats.totalEntries,
            currentlyActive: stats.currentlyActive,
            percentageOfPlacements: stats.totalEntries > 0 ? (stats.placedStudents / stats.totalEntries) * 100 : 0,
            'Average Duration': averageDuration,
            earliestSnapshot: stats.earliestSnapshot ? stats.earliestSnapshot.toLocaleDateString() : 'N/A',
        };
    });
};

export const computeStatistics = (data) => {
    const totalEntries = data.length;
    let placedStudents = 0;
    let currentlyActive = 0;
    let totalYears = 0;
    let yearsCount = 0;
    let earliestSnapshot = null;
    let programLink = data[0].URL;
    let placementLink = data[0].PlacementURL;
    let numberOfSnapshots = data[0].Snapshots.length;

    data.forEach((entry) => {
        if (entry.Placement === true) {
            placedStudents += 1;
        }
        if (entry.Active === true) {
            currentlyActive += 1;
        }

        if (entry.Years && !entry.Active) {
            totalYears += entry.Years;
            yearsCount += 1;
        }

        if (entry.Start_Date) {
            const startDate = new Date(entry.Start_Date);
            if (!earliestSnapshot || startDate < earliestSnapshot) {
                earliestSnapshot = startDate;
            }
        }
        // programLink = entry.URL;
    });

    const percentageOfPlacements = totalEntries > 0 ? (placedStudents / totalEntries) * 100 : 0;
    const averageDuration = yearsCount > 0 ? (totalYears / yearsCount).toFixed(2) : 'N/A';

    return {
        totalEntries,
        percentageOfPlacements: percentageOfPlacements > 0 ? percentageOfPlacements.toFixed(2) : '0.00',
        currentlyActive,
        earliestSnapshot: earliestSnapshot ? earliestSnapshot.toLocaleDateString() : 'N/A',
        'Average Duration': averageDuration,
        programLink: programLink,
        placementLink: placementLink,
        numberOfSnapshots: numberOfSnapshots,
    };
};

export const formatColumnName = (name) => {
    if (name === 'totalEntries') {
        return 'Total Entries';
    }
    return name.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
};