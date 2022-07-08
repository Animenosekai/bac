interface ArrayComparisonResult {
    index: number;
    similarity: number;
}

export function compare(first: string, second: string) {
    /*
        Dice's Coefficient Algorithm Implementation
        Based on https://github.com/aceakash/string-similarity
    */
    first = first.replace(/\s+/g, "");
    second = second.replace(/\s+/g, "");

    if (first === second) return 1; // identical or empty
    if (first.length < 2 || second.length < 2) return 0; // if either is a 0-letter or 1-letter string

    let firstBigrams = new Map();
    for (let i = 0; i < first.length - 1; i++) {
        const bigram = first.substring(i, i + 2);
        const count = firstBigrams.has(bigram) ? firstBigrams.get(bigram) + 1 : 1;

        firstBigrams.set(bigram, count);
    }

    let intersectionSize = 0;
    for (let i = 0; i < second.length - 1; i++) {
        const bigram = second.substring(i, i + 2);
        const count = firstBigrams.has(bigram) ? firstBigrams.get(bigram) : 0;

        if (count > 0) {
            firstBigrams.set(bigram, count - 1);
            intersectionSize++;
        }
    }

    return (2.0 * intersectionSize) / (first.length + second.length - 2);
}

export function compareArray(searchTerm: string, searchingSet: string[]) {
    /* Compares every element in the array and returns ArrayComparisonResult[] */
    let results = [];
    for (let i = 0; i < searchingSet.length; i++) {
        const similarity = compare(searchTerm, searchingSet[i]);
        results.push({ index: i, similarity: similarity });
    }
    return results;
}

export const sortCompare = (
    a: { similarity: number },
    b: { similarity: number }
) => {
    /* this sorting algorithm is reversed */
    if (a.similarity > b.similarity) {
        return -1;
    } else if (a.similarity < b.similarity) {
        return 1;
    }
    return 0;
};

export const sort = (searchTerm: string, searchingSet: string[]) => {
    /* Sorts the given array with the best results at the beginning and returns ArrayComparisonResult[] */
    let results = [];
    for (let i = 0; i < searchingSet.length; i++) {
        const similarity = compare(searchTerm, searchingSet[i]);
        results.push({ index: i, similarity: similarity });
    }
    return results.sort(sortCompare);
};

export const similar = <T>(
    array: Array<T>,
    searchTerm: string,
    check: Array<string>
) => {
    if (searchTerm.replace(" ", "") === "") {
        // if nothing is entered, return everything
        return array;
    }
    searchTerm = searchTerm.toLowerCase();
    let results = [];
    for (let i = 0; i < array.length; i++) {
        let checks = [];
        for (let paramIndex in check) {
            checks.push(arrayElement(array[i], check[paramIndex]).toLowerCase());
        }
        if (checks.length > 0) {
            let element = sort(searchTerm, checks)[0];
            element.index = i;
            results.push(element);
        }
    }
    results.sort(sortCompare);
    let mappedResults = [];
    for (let resultIndex in results) {
        mappedResults.push(array[results[resultIndex].index]);
    }
    return mappedResults.slice(0, 5); // returning the experimental string similarity results
};

const arrayElement = <T>(arrayItem: T, element: string) => {
    let newElement = element.split(".");
    newElement.map((item) => (arrayItem = arrayItem[item]));
    return typeof arrayItem !== "string" ? "" : arrayItem; // verify that it's not undefined
};
