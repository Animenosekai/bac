import data from "data/subjects.json";

export const subjectName = (name: string) => {
    const result = data[name]
    return result ? result.short : name
}