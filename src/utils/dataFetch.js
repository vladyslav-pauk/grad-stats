export const fetchVersions = async () => {
    const response = await fetch('/data/versions.json');
    const versionData = await response.json();
    return versionData.latest_version;
};

export const fetchStudentData = async (latestVersion) => {
    const response = await fetch(`/data/student_data_v${latestVersion}.json`);
    const data = await response.json();
    return data;
};