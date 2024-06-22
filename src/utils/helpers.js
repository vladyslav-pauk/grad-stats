const updateProgramSummary = (programs, entry) => {
    const program = entry.University;
    if (!programs[program]) {
        programs[program] = {
            totalEntries: 0,
            placedStudents: 0,
            currentlyActive: 0,
            totalYears: 0,
            yearsCount: 0,
            earliestSnapshot: null,
            snapshots: []
        };
    }
    programs[program].totalEntries += 1;
    if (entry.Placement === true) {
        programs[program].placedStudents += 1;
    }
    if (entry.Active === true) {
        programs[program].currentlyActive += 1;
    }
    const startDate = new Date(entry.Start_Date);
    if (!programs[program].earliestSnapshot || startDate <= programs[program].earliestSnapshot) {
        programs[program].earliestSnapshot = startDate;
    }
    if (entry.Snapshots && entry.Snapshots.length > 0) {
        entry.Snapshots.forEach(snapshot => {
            const snapshotDate = extractDateFromUrl(snapshot).date;
            programs[program].snapshots.push(snapshotDate);
        });
        programs[program].snapshots.sort((a, b) => a - b);
    }
};

const extractDateFromUrl = (url) => {
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

const computeMiddleDate = (date1, date2) => {
    const time1 = date1.getTime();
    const time2 = date2.getTime();
    const middleTime = (time1 + time2) / 2;
    return new Date(middleTime);
};

const updateDatesAndCalculateAverage = (data, programs) => {
    data.forEach(entry => {
        const program = programs[entry.University];

        // Preserve the original start date in a new field
        if (!entry.originalStartDate) {
            entry.originalStartDate = entry.Start_Date;
        }

        // Preserve the original end date in a new field
        if (!entry.originalEndDate) {
            entry.originalEndDate = entry.End_Date;
        }

        // Update Start_Date to be in the middle between the original start date and the nearest preceding snapshot
        if (entry.Start_Date !== 'N/A' && program.snapshots.length > 0) {
            const originalStartDate = new Date(entry.originalStartDate);
            const precedingSnapshot = program.snapshots.slice().reverse().find(snapshot => snapshot < originalStartDate);
            if (precedingSnapshot) {
                entry.Start_Date = computeMiddleDate(precedingSnapshot, originalStartDate).toLocaleDateString();
            }
        }

        // Update End_Date to be in the middle between the original end date and the nearest later snapshot
        if (!entry.Active && entry.End_Date !== 'N/A' && program.snapshots.length > 0) {
            const originalEndDate = new Date(entry.originalEndDate);
            const laterSnapshot = program.snapshots.find(snapshot => snapshot > originalEndDate);
            if (laterSnapshot) {
                entry.End_Date = computeMiddleDate(originalEndDate, laterSnapshot).toLocaleDateString();
            }
        }

        // Set Start_Date to 'N/A' if it matches the earliest snapshot
        if (program && new Date(entry.Start_Date).toLocaleDateString() === program.earliestSnapshot.toLocaleDateString()) {
            entry.Start_Date = 'N/A';
        }

        // Set End_Date to 'N/A' if the student is active
        if (entry.Active) {
            entry.End_Date = 'N/A';
        }

        // Calculate and update the Years field
        const startDate = new Date(entry.Start_Date);
        const endDate = new Date(entry.End_Date);
        if (entry.Start_Date === 'N/A' || isNaN(startDate) || isNaN(endDate)) {
            entry.Years = 'N/A';
        } else {
            entry.Years = ((endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25)).toFixed(2);
        }
    });

    // Recalculate the total years and years count based on updated dates
    Object.keys(programs).forEach(programName => {
        const program = programs[programName];
        program.totalYears = 0;
        program.yearsCount = 0;
    });

    data.forEach(entry => {
        const startDate = new Date(entry.Start_Date);
        const endDate = new Date(entry.End_Date);

        if (!isNaN(startDate) && !isNaN(endDate) && entry.Start_Date !== 'N/A' && entry.End_Date !== 'N/A') {
            const durationInYears = (endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25);
            const program = programs[entry.University];
            if (!entry.Active && entry.Start_Date !== 'N/A' && entry.End_Date !== 'N/A') {
                program.totalYears += durationInYears;
                program.yearsCount += 1;
            }
        }
    });

    return programs;
};

export const computeProgramIndex = (data) => {
    const programs = {};

    // Update the program summaries
    data.forEach(entry => updateProgramSummary(programs, entry));

    // Update dates and recalculate the average duration
    updateDatesAndCalculateAverage(data, programs);

    return Object.keys(programs).map(program => {
        const stats = programs[program];
        const averageDuration = stats.yearsCount > 0 ? (stats.totalYears / stats.yearsCount).toFixed(2) : 'N/A';
        const placementRate = (stats.placedStudents / stats.totalEntries) * 100;
        const originalStartDate = data.find(entry => entry.University === program).originalStartDate;
        return {
            program: program,
            totalEntries: stats.totalEntries,
            currentlyActive: stats.currentlyActive,
            percentageOfPlacements: placementRate.toFixed(2),
            averageDuration: averageDuration,
            originalStartDate: originalStartDate,
        };
    });
};

export const computeProgramSummary = (data) => {
    const totalEntries = data.length;
    let placedStudents = 0;
    let currentlyActive = 0;
    let totalYears = 0;
    let yearsCount = 0;
    let earliestSnapshot = null;
    let programLink = data[0].URL;
    let placementLink = data[0].PlacementURL;

    const snapshotMap = new Map();
    data.forEach((entry) => {
        if (entry.Snapshots && entry.Snapshots.length > 0) {
            entry.Snapshots.forEach((snapshot) => {
                const { date, formattedDate } = extractDateFromUrl(snapshot);
                if (!snapshotMap.has(formattedDate)) {
                    snapshotMap.set(formattedDate, { date, formattedDate, url: snapshot, count: 0 });
                }
                const currentEntry = snapshotMap.get(formattedDate);
                snapshotMap.set(formattedDate, { date, formattedDate, url: snapshot, count: currentEntry.count + 1 });
            });
        }
    });
    const numberOfSnapshots = snapshotMap.size;

    data.forEach((entry) => {
        if (entry.Placement === true) {
            placedStudents += 1;
        }
        if (entry.Active === true) {
            currentlyActive += 1;
        }
        if (entry.Start_Date && entry.Start_Date !== 'N/A') {
            const startDate = new Date(entry.Start_Date);
            if (!earliestSnapshot || startDate < earliestSnapshot) {
                earliestSnapshot = startDate;
            }
        }
    });

    // Update dates and recalculate the average duration
    const programs = {};
    data.forEach(entry => updateProgramSummary(programs, entry));
    updateDatesAndCalculateAverage(data, programs);

    data.forEach(entry => {
        const startDate = new Date(entry.Start_Date);
        const endDate = new Date(entry.End_Date);

        if (!isNaN(startDate) && !isNaN(endDate) && entry.Start_Date !== 'N/A' && entry.End_Date !== 'N/A') {
            const durationInYears = (endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25);
            if (!entry.Active && entry.Start_Date !== 'N/A' && entry.End_Date !== 'N/A') {
                totalYears += durationInYears;
                yearsCount += 1;
            }
        }
    });

    const percentageOfPlacements = totalEntries > 0 ? (placedStudents / totalEntries) * 100 : 0;
    const averageDuration = yearsCount > 0 ? (totalYears / yearsCount).toFixed(2) : 'N/A';
    const originalStartDate = data.find(entry => entry.University === data[0].University).originalStartDate;

    return {
        totalEntries,
        percentageOfPlacements: percentageOfPlacements.toFixed(2),
        currentlyActive,
        originalStartDate: originalStartDate,
        averageDuration: averageDuration,
        programLink: programLink,
        placementLink: placementLink,
        numberOfSnapshots: numberOfSnapshots,
    };
};

export const formatValue = (value, row, column) => {
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    if (typeof value === 'number') {
        return value.toFixed(1);
    }
    if (typeof value === 'string') {
        return value;
    }
};

export const formatColumnName = (name) => {
    if (name === 'totalEntries') {
        return 'Total Entries';
    }
    if (name === 'Years') {
        return 'Time-to-Degree';
    }
    if (name === 'Active') {
        return 'Enrolled';
    }
    return name.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
};
