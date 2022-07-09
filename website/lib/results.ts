export type Results = Result[]

export interface Result {
    academy: string
    session: number
    birthday: string
    ine: string
    birthplace: Birthplace
    gender: string
    address: Address
    school: string
    jury: number
    epreuves: Epreuves
    optionnel: Optionnel
    mention?: string
    class: string
    candidateNumber: number
    registrationNumber: number
    firstNames: string[]
    lastName: string
    usageName?: string
    birthdayTimestamp: number
    schoolID: string
    controleContinu: ControleContinu
    calculResultat: CalculResultat
}

export interface Birthplace {
    department?: number
    city: string
    country: string
    foreign: boolean
}

export interface Address {
    raw: string
    city: string
    postalCode: number
}

export interface Epreuves {
    philosophy: Grade
    options: string[]
    total: Total
    frenchWritten: Grade
    frenchSpeaking: Grade
    grandOral: Grade
    firstOption: GradeWithName
    secondOption: GradeWithName
}

export interface Grade {
    coefficient: number
    grade: number
    points: number
}

export interface Total {
    coefficient: number
    points: number
}

export interface GradeWithName {
    coefficient: number
    grade: number
    points: number
    name: string
}


export interface Optionnel {
    options: string[]
    firstOption?: GradeWithName
    secondOption?: GradeWithName
    thirdOption?: GradeWithName
}

export interface ControleContinu {
    premiere: Premiere
    terminale: Terminale
    total: Total
    optionName: string
    firstLanguage: string
    secondLanguage: string
}

export interface Premiere {
    history: Grade
    ensc: Grade
    option: GradeWithName
    all: Grade
    firstLanguage: GradeWithName
    secondLanguage: GradeWithName
}

export interface Terminale {
    history: Grade
    emc: Grade
    ensc: Grade
    sport?: Grade
    firstLanguage: GradeWithName
    secondLanguage: GradeWithName
}


export interface CalculResultat {
    epreuves: Total
    optionnel: Total
    jury: Total
    total: Total
    average: number
    controleContinu: Total
}