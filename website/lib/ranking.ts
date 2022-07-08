import data from "data/results";

export const ranking = () => {
    return data().sort((a, b) => a.calculResultat.average < b.calculResultat.average ? 1 : a.calculResultat.average === b.calculResultat.average ? 0 : -1)
}