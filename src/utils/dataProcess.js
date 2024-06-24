import { extractDateFromUrl } from './helpers';

const initialize_programs = (data) => {
    const programs = {};
    data.forEach(entry => {
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
    });
    return programs;
};

const updateStatus = (programs, data) => {
    data.forEach(entry => {
        const program = entry.University;
        programs[program].totalEntries += 1;
        if (entry.Placement === true) {
            programs[program].placedStudents += 1;
        }
        if (entry.Active === true) {
            programs[program].currentlyActive += 1;
        }
    });
};


const updateSnapshotInfo = (programs, data) => {
    data.forEach(entry => {
        const program = entry.University;
        if (!programs[program].earliestSnapshot || new Date(entry.Start_Date) <= new Date(programs[program].earliestSnapshot)) {
            programs[program].earliestSnapshot = new Date(entry.Start_Date).toLocaleDateString();
        }

        if (entry.Snapshots && entry.Snapshots.length > 0) {
            entry.Snapshots.forEach(snapshot => {
                const snapshotDate = extractDateFromUrl(snapshot).date;
                programs[program].snapshots.push(snapshotDate);
            });
            programs[program].snapshots.sort((a, b) => new Date(a) - new Date(b));
        }
    });
};

const computeMiddleDate = (date1, date2) => {
    const time1 = date1.getTime();
    const time2 = date2.getTime();
    const middleTime = (time1 + time2) / 2;
    return new Date(middleTime).toLocaleDateString();
};

export const updateDates = (data, programs) => {
    data.forEach(entry => {
        const program = programs[entry.University];
        const startDate = new Date(entry.Start_Date);
        const endDate = new Date(entry.End_Date);

        const precedingSnapshot = program.snapshots.slice().reverse().find(snapshot => new Date(snapshot) < startDate);
        if (precedingSnapshot) {
            entry.enrollmentDate = computeMiddleDate(new Date(precedingSnapshot), startDate);
        } else {
            entry.enrollmentDate = `< ${startDate.toLocaleDateString()}`;
        }

        if (!entry.Active) {
            const laterSnapshot = program.snapshots.find(snapshot => new Date(snapshot) > endDate);
            if (laterSnapshot) {
                entry.completionDate = computeMiddleDate(endDate, new Date(laterSnapshot));
            }
        } else {
            entry.completionDate = `> ${endDate.toLocaleDateString()}`;
        }
    });
    return data;
};

export const updateTimeToDegree = (data, programs) => {
    Object.keys(programs).forEach(programName => {
        const program = programs[programName];
        program.totalYears = 0;
        program.yearsCount = 0;
    });

    const { totalYears, yearsCount } = calculateAverageYearsToDegree(data);

    data.forEach(entry => {
        const program = programs[entry.University];
        const startDate = new Date(entry.enrollmentDate.replace('< ', ''));
        const endDate = new Date(entry.completionDate.replace('> ', ''));
        const durationInYears = (endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25);

        program.totalYears += durationInYears;
        program.yearsCount += 1;

        if (!entry.enrollmentDate.includes('<') && !entry.completionDate.includes('>')) {
            entry.timeToDegree = durationInYears.toFixed(2);
        } else {
            entry.timeToDegree = `> ${durationInYears.toFixed(2)}`;
        }
    });

    return programs;
};

const calculateAverageYearsToDegree = (data) => {
    let totalYears = 0;
    let yearsCount = 0;

    data.forEach(entry => {
        const startDate = new Date(entry.enrollmentDate.replace('< ', ''));
        const endDate = new Date(entry.completionDate.replace('> ', ''));
        const durationInYears = (endDate - startDate) / (1000 * 60 * 60 * 24 * 365.25);

        totalYears += durationInYears;
        yearsCount += 1;

        if (!entry.enrollmentDate.includes('<') && !entry.completionDate.includes('>')) {
            entry.timeToDegree = durationInYears.toFixed(2);
        } else {
            entry.timeToDegree = `> ${durationInYears.toFixed(2)}`;
        }
    });

    const averageDuration = yearsCount > 0 ? (totalYears / yearsCount).toFixed(2) : 'N/A';
    return { totalYears, yearsCount, averageDuration };
};

export const computeProgramIndex = (data) => {
    const programs = initialize_programs(data);
    updateStatus(programs, data);
    updateSnapshotInfo(programs, data);
    updateDates(data, programs);
    updateTimeToDegree(data, programs);

    return Object.keys(programs).map(program => {
        const stats = programs[program];
        const averageDuration = stats.yearsCount > 0 ? (stats.totalYears / stats.yearsCount).toFixed(2) : 'N/A';
        const placementRate = ((stats.placedStudents / stats.totalEntries) * 100).toFixed(2);
        const earliestSnapshot = stats.earliestSnapshot;
        return {
            program: program,
            totalEntries: stats.totalEntries,
            currentlyActive: stats.currentlyActive,
            percentageOfPlacements: placementRate,
            averageDuration: averageDuration,
            earliestSnapshot: earliestSnapshot,
        };
    });
};

export const computeProgramSummary = (data) => {
    const totalEntries = data.length;
    let placedStudents = 0;
    let currentlyActive = 0;
    let earliestSnapshot = null;
    let programLink = data.length > 0 ? data[0].URL : '';
    let placementLink = data.length > 0 ? data[0].PlacementURL : '';

    const uniqueSnapshotDates = new Set();

    data.forEach(entry => {
        if (entry.Placement) {
            placedStudents += 1;
        }
        if (entry.Active) {
            currentlyActive += 1;
        }

        if (!earliestSnapshot || new Date(entry.Start_Date) < new Date(earliestSnapshot)) {
            earliestSnapshot = entry.Start_Date;
        }

        if (entry.Snapshots && entry.Snapshots.length > 0) {
            entry.Snapshots.forEach(snapshot => {
                const { date } = extractDateFromUrl(snapshot);
                uniqueSnapshotDates.add(date.toDateString()); // Add unique date strings
            });
        }
    });

    const { totalYears, yearsCount, averageDuration } = calculateAverageYearsToDegree(data);

    const percentageOfPlacements = totalEntries > 0 ? ((placedStudents / totalEntries) * 100).toFixed(2) : '0.00';

    return {
        totalEntries,
        percentageOfPlacements,
        currentlyActive,
        earliestSnapshot: earliestSnapshot ? new Date(earliestSnapshot).toLocaleDateString() : 'N/A',
        averageDuration,
        programLink,
        placementLink,
        numberOfSnapshots: uniqueSnapshotDates.size, // Number of unique snapshot dates
    };
};