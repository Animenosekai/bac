import { Chart, fr } from "components/chart";
import { IconAward, IconTrash, IconUserX } from "@tabler/icons";

import { Button } from "components/ui/button";
import Link from "next/link";
import { Options } from "components/cards/options";
import { Rank } from "components/cards/rank";
import { range } from "utils/range";
import { subjectName } from "utils/subject";
import { useData } from "contexts/data";
import { useRouter } from "next/router"

const CHART_COLORS = ["#008FFB", "#00E396", "#FEB019", "#FF4560", "#775DD0", "#4B5B29"]

const Student = () => {
    const router = useRouter();
    const { ine } = router.query;
    const { data, removeStudent } = useData();
    const student = data.find(val => val.ine === ine)

    if (!student) {
        return <div className="flex flex-col justify-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <div className="flex flex-row space-x-5 justify-center">
                <IconUserX className="scale-150" />
                <span className="text-xl font-semibold">Nous n'avons pas pu trouver l'INE</span>
            </div>
            <Link href="/database" passHref={true}>
                <a className="mt-5 text-blue-500 hover:text-blue-700 transition self-center">Retour à la base de données</a>
            </Link>
        </div>
    }

    const currentRanking = data.sort((a, b) => a.calculResultat.average < b.calculResultat.average ? 1 : a.calculResultat.average === b.calculResultat.average ? 0 : -1)
    const currentRank = currentRanking.findIndex(val => val.ine === ine) + 1

    let bestMark = student.epreuves.frenchWritten.grade
    let bestMarkSubject = "Français Écrit"
    Array.from([{ id: "frenchSpeaking", name: "Français Oral" }, { id: "philosophy", name: "Philosophie" }, { id: "grandOral", name: "Grand Oral" }, { id: "firstOption", name: student.epreuves.firstOption.name }, { id: "secondOption", name: student.epreuves.secondOption.name }]).forEach(val => {
        if (student.epreuves[val.id].grade > bestMark) {
            bestMark = student.epreuves[val.id].grade
            bestMarkSubject = subjectName(val.name)
        }
    })

    const performance = {}

    let filtered = data.filter(s => s.epreuves.options.includes(student.epreuves.firstOption.name))

    const firstResults =
        filtered
            .sort((a, b) => {
                const aField = a.epreuves.firstOption.name === student.epreuves.firstOption.name
                    ? "firstOption"
                    : "secondOption"
                const bField = b.epreuves.firstOption.name === student.epreuves.firstOption.name
                    ? "firstOption"
                    : "secondOption"
                return a.epreuves[aField].grade < b.epreuves[bField].grade
                    ? 1
                    : a.epreuves[aField].grade === b.epreuves[bField].grade
                        ? 0
                        : -1
            })
    let bestPerf = firstResults.findIndex(val => val.epreuves.firstOption.grade === student.epreuves.firstOption.grade) + 1
    let bestPerfSubject = subjectName(student.epreuves.firstOption.name)
    performance[bestPerfSubject] = { rank: bestPerf, total: filtered.length }

    filtered = data.filter(s => s.epreuves.options.includes(student.epreuves.secondOption.name))

    const secondResults =
        filtered
            .sort((a, b) => {
                const aField = a.epreuves.firstOption.name === student.epreuves.secondOption.name
                    ? "firstOption"
                    : "secondOption"
                const bField = b.epreuves.firstOption.name === student.epreuves.secondOption.name
                    ? "firstOption"
                    : "secondOption"
                return a.epreuves[aField].grade < b.epreuves[bField].grade
                    ? 1
                    : a.epreuves[aField].grade === b.epreuves[bField].grade
                        ? 0
                        : -1
            })
    const secondIndex = secondResults.findIndex(val => val.epreuves.secondOption.grade === student.epreuves.secondOption.grade) + 1
    if (bestPerf > secondIndex) {
        bestPerf = secondIndex
        bestPerfSubject = subjectName(student.epreuves.secondOption.name)
    }
    performance[subjectName(student.epreuves.secondOption.name)] = { rank: secondIndex, total: filtered.length }


    Array.from([{ id: "frenchWritten", name: "Français Écrit" }, { id: "frenchSpeaking", name: "Français Oral" }, { id: "philosophy", name: "Philosophie" }, { id: "grandOral", name: "Grand Oral" }]).forEach(val => {
        const results = data.filter(val => val).sort((a, b) => a.epreuves[val.id].grade < b.epreuves[val.id].grade ? 1 : a.epreuves[val.id].grade === b.epreuves[val.id].grade ? 0 : -1)
        const index = results.findIndex(current => current.epreuves[val.id].grade === student.epreuves[val.id].grade) + 1
        if (bestPerf > index) {
            bestPerf = index
            bestPerfSubject = subjectName(val.name)
        }
        performance[subjectName(val.name)] = { rank: index, total: data.length }
    })

    const performanceSubjects = Object.keys(performance)

    return <div className="flex flex-col p-5">
        <h1 className="text-2xl font-semibold mx-10 mt-10">Informations</h1>
        <div className="mx-10 my-4 p-5 flex flex-col">
            <div className="flex flex-row items-center">
                <span className="text-lg font-medium mr-1">{student.lastName} {student.firstNames[0]}</span>
                {
                    student.firstNames.length > 0 && <div className="mx-1">{' '}<span className="text-gray-500 font-medium">{student.firstNames.slice(1).join(" ")}</span></div>
                }
            </div>
            {
                student.usageName && <span>{`Nom d'usage: ${student.usageName}`}</span>
            }
            <span>
                {
                    student.gender === "MALE"
                        ? "Homme"
                        : "Femme"
                }
            </span>
            <span>{`Né${student.gender === "FEMALE" ? "e" : ""} le ${new Date(student.birthday).toLocaleDateString("fr")} à ${student.birthplace.city} en ${student.birthplace.country}`}</span>
            <span>{`Réside à ${student.address.city} (${student.address.postalCode})`}</span>
            {/* <span>{`Étudie en classe de ${student.class} au lycée ${student.school}`}</span> */}
            <span>{`Étudie en classe de ${student.class}`}</span>
            <span>{`INE: ${student.ine}・N° de candidat: ${student.candidateNumber}・N° d'inscription: ${student.registrationNumber}`}</span>
        </div>
        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold">Overview</h1>
            <div className='flex flex-row bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center flex-wrap w-4/5 justify-around'>
                {
                    [{ field: "controleContinu", name: "Contrôle Continu" }, { field: "epreuves", name: "Épreuves Écrites" }, { field: "optionnel", name: "Options" }, { field: "jury", name: "Points du Jury" }, { field: "total", name: "Total" }].map((element, i) => {
                        const result = student.calculResultat[element.field].points / student.calculResultat[element.field].coefficient
                        return <div className="flex flex-col justify-center" key={i}>
                            <Chart type="radialBar" width={150} height={150} options={{
                                plotOptions: {
                                    radialBar: {
                                        hollow: {
                                            margin: 15,
                                            size: "60%"
                                        },
                                        dataLabels: {
                                            show: true,
                                            name: {
                                                show: true,
                                                offsetY: 20,
                                                fontSize: "80%",
                                                color: "#111",
                                                fontWeight: "thin"
                                            },
                                            value: {
                                                color: "#111",
                                                offsetY: -15,
                                                fontSize: "125%",
                                                formatter: (_) => { return (element.field === "jury" ? "+ " : "") + (student.calculResultat[element.field].coefficient === 0 ? "0" : String(Math.round((result) * 100) / 100)) },
                                                show: true
                                            }
                                        }
                                    }
                                },
                                fill: {
                                    colors: [
                                        element.field === "jury"
                                            ? "rgb(94,202,117)"
                                            : result > 14
                                                ? "rgb(94,202,117)"
                                                : result > 12
                                                    ? "rgb(243,170,63)"
                                                    : "rgb(236,93,77)"
                                    ]
                                },
                                stroke: {
                                    lineCap: "round"
                                },
                                labels: [`Coef ${student.calculResultat[element.field].coefficient}`]
                            }} series={[result * 5]} /> {/* (result / 20) * 100 */}
                            <span className="font-semibold self-center">{element.name}</span>
                        </div>
                    })
                }
                {
                    student.mention && <div className="flex flex-col rounded w-max p-4 self-center">
                        <div className="self-center text-gray-600" style={{
                            color: student.mention.startsWith("Très Bien")
                                ? "#FFD700"
                                : student.mention === "Bien"
                                    ? "rgb(75, 85, 99)"
                                    : "#C36B29"
                        }} >
                            <IconAward size={50} />
                        </div>
                        <div className="self-center">
                            <span className="font-medium">{student.mention}</span>
                        </div>
                    </div>
                }
            </div>

        </div>

        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold">Options choisies</h1>
            <div className="flex space-x-4 space-y-4 flex-row flex-wrap justify-around">
                <Options title="Spécialités" options={[
                    student.controleContinu.optionName,
                    ...student.epreuves.options
                ]} />
                <Options title="Langues Vivantes" options={[
                    student.controleContinu.firstLanguage,
                    student.controleContinu.secondLanguage
                ]} />
                {
                    student.optionnel.options.length > 0 && <Options title="Options" options={student.optionnel.options} />
                }
            </div>
        </div>

        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold">Contrôle Continu</h1>
            <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>
                <Chart options={{
                    // xaxis: { type: 'category', categories: ["Histoire", "EMC", "ENSC", "Sport", student.controleContinu.firstLanguage, student.controleContinu.secondLanguage, student.controleContinu.optionName, "Bulletins"] },
                    xaxis: { type: 'category' },
                    yaxis: { min: 0, max: 20 },
                    markers: {
                        size: 5,
                        hover: { size: 9 }
                    },
                    title: {
                        text: "Notes obtenues au contrôle continu"
                    },
                    dataLabels: { enabled: false },
                    stroke: { curve: 'smooth' },
                    chart: {
                        locales: [fr],
                        defaultLocale: "fr"
                    }
                }} type="area" height={350} series={
                    [
                        {
                            name: "1ère",
                            data: [
                                { x: 'Histoire', y: student.controleContinu.premiere.history.grade },
                                { x: "EMC", y: null },
                                { x: 'ENSC', y: student.controleContinu.premiere.ensc.grade },
                                { x: "Sport", y: null },
                                { x: subjectName(student.controleContinu.firstLanguage), y: student.controleContinu.premiere.firstLanguage?.grade },
                                { x: subjectName(student.controleContinu.secondLanguage), y: student.controleContinu.premiere.secondLanguage?.grade },
                                { x: subjectName(student.controleContinu.optionName), y: student.controleContinu.premiere.option?.grade },
                                { x: "Bulletins", y: student.controleContinu.premiere.all?.grade }
                            ],
                        },
                        {
                            name: "Terminale",
                            data: [
                                { x: "Histoire", y: student.controleContinu.terminale.history?.grade },
                                { x: "EMC", y: student.controleContinu.terminale.emc?.grade },
                                { x: "ENSC", y: student.controleContinu.terminale.ensc?.grade },
                                { x: "Sport", y: student.controleContinu.terminale.sport?.grade },
                                { x: subjectName(student.controleContinu.firstLanguage), y: student.controleContinu.terminale.firstLanguage?.grade },
                                { x: subjectName(student.controleContinu.secondLanguage), y: student.controleContinu.terminale.secondLanguage?.grade },
                                { x: subjectName(student.controleContinu.optionName), y: null },
                                { x: "Bulletins", y: null }
                            ]
                        }
                    ]
                } />
            </div>
        </div>

        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold">Épreuves</h1>
            <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>
                <Chart options={{
                    // xaxis: { type: 'category', categories: ["Histoire", "EMC", "ENSC", "Sport", student.controleContinu.firstLanguage, student.controleContinu.secondLanguage, student.controleContinu.optionName, "Bulletins"] },
                    xaxis: { type: 'category' },
                    yaxis: { min: 0, max: 20 },
                    markers: {
                        size: 5,
                        hover: { size: 9 }
                    },
                    title: {
                        text: "Notes obtenues aux différentes épreuves"
                    },
                    dataLabels: { enabled: false },
                    stroke: { curve: 'smooth' },
                    chart: {
                        locales: [fr],
                        defaultLocale: "fr"
                    }
                }} type="area" height={350} series={
                    [
                        {
                            name: "Note",
                            data: [
                                { x: 'Français Écrit', y: student.epreuves.frenchWritten.grade },
                                { x: 'Français Oral', y: student.epreuves.frenchSpeaking.grade },
                                { x: 'Philosophie', y: student.epreuves.philosophy.grade },
                                { x: 'Grand Oral', y: student.epreuves.grandOral.grade },
                                { x: subjectName(student.epreuves.firstOption.name), y: student.epreuves.firstOption.grade },
                                { x: subjectName(student.epreuves.secondOption.name), y: student.epreuves.secondOption.grade }
                            ],
                        }
                    ]
                } />
            </div>
        </div>

        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold" id="Classement">Classement</h1>
            <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>
                <Rank data={currentRanking.slice(currentRank - Math.min(currentRank, 5), currentRank + 5).map(val => { return { id: val.ine, name: `${val.lastName} ${val.firstNames[0]}`, link: `/database/student/${val.ine}#Classement` } })} selected={student.ine} selectedRank={currentRank} increment={2} />
            </div>
        </div>

        <div className="m-10 flex flex-col space-y-10">
            <h1 className="text-2xl font-semibold">Performance</h1>
            <div className="flex flex-row space-x-2 flex-wrap justify-around">
                <div className="bg-gray-100 bg-opacity-80 rounded-lg p-4">
                    <h2 className="text-lg font-medium">Meilleure Note</h2>
                    <span><b>{bestMark}</b>{" en "}<b>{bestMarkSubject}</b></span>
                </div>
                <div className="bg-gray-100 bg-opacity-80 rounded-lg p-4">
                    <h2 className="text-lg font-medium">Meilleur Rang</h2>
                    <span><b>#{bestPerf}</b>{" en "}<b>{bestPerfSubject}</b></span>
                </div>
            </div>

            <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>
                <Chart options={{
                    // xaxis: { type: 'category', categories: ["Histoire", "EMC", "ENSC", "Sport", student.controleContinu.firstLanguage, student.controleContinu.secondLanguage, student.controleContinu.optionName, "Bulletins"] },
                    xaxis: { type: 'category' },
                    yaxis: { min: 0, max: 100 },
                    markers: {
                        size: 5,
                        hover: { size: 9 }
                    },
                    title: {
                        text: "Rang obtenu aux différentes épreuves, normalisé de sorte que le premier soit à 100%"
                    },
                    tooltip: {
                        y: {
                            formatter: (_, { dataPointIndex }) => { return performance[performanceSubjects[dataPointIndex]].rank }
                        }
                    },
                    dataLabels: { enabled: false },
                    stroke: { curve: 'smooth' },
                    chart: {
                        locales: [fr],
                        defaultLocale: "fr"
                    }
                }} type="area" height={350} series={
                    [
                        {
                            name: "Rang",
                            data: [
                                ...performanceSubjects.map(val => {
                                    return { x: val, y: Math.round(((performance[val].total - performance[val].rank) / performance[val].total) * 100) }
                                })
                            ],
                        }
                    ]
                } />
            </div>
            <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>
                <Chart options={{
                    // xaxis: { type: 'category', categories: ["Histoire", "EMC", "ENSC", "Sport", student.controleContinu.firstLanguage, student.controleContinu.secondLanguage, student.controleContinu.optionName, "Bulletins"] },
                    xaxis: { type: "numeric", categories: range(20) },
                    yaxis: { min: 0 },
                    dataLabels: { enabled: false },
                    stroke: { curve: 'smooth' },
                    chart: {
                        locales: [fr],
                        defaultLocale: "fr"
                    },
                    title: {
                        text: "Distribution des notes aux épreuves du baccalauréat"
                    },
                    annotations: {
                        xaxis: range(6).map(index => {
                            const subjects = ["frenchWritten", "frenchSpeaking", "philosophy", "grandOral", "firstOption", "secondOption"]
                            const subject = subjects[index]
                            return {
                                x: student.epreuves[subject].grade,
                                borderColor: CHART_COLORS[index % CHART_COLORS.length],
                                label: {
                                    borderColor: CHART_COLORS[index % CHART_COLORS.length],
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: CHART_COLORS[index % CHART_COLORS.length]
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: subject === "frenchWritten"
                                        ? "Français Écrit"
                                        : subject === "frenchSpeaking"
                                            ? "Français Oral"
                                            : subject === "philosophy"
                                                ? "Philosophie"
                                                : subject === "grandOral"
                                                    ? "Grand Oral"
                                                    : subject === "firstOption"
                                                        ? subjectName(student.epreuves.firstOption.name)
                                                        : subjectName(student.epreuves.secondOption.name)
                                }
                            }
                        })
                    }
                }} type="area" height={350} series={
                    [
                        {
                            name: "Français Écrit",
                            data: range(21).map(val => {
                                return { x: val, y: data.filter(s => s.epreuves.frenchWritten.grade === val).length }
                            }),
                            color: CHART_COLORS[0 % CHART_COLORS.length]
                        },
                        {
                            name: "Français Oral",
                            data: range(21).map(val => {
                                return { x: val, y: data.filter(s => s.epreuves.frenchSpeaking.grade === val).length }
                            }),
                            color: CHART_COLORS[1 % CHART_COLORS.length]
                        },
                        {
                            name: "Philosophie",
                            data: range(21).map(val => {
                                return { x: val, y: data.filter(s => s.epreuves.philosophy.grade === val).length }
                            }),
                            color: CHART_COLORS[2 % CHART_COLORS.length]
                        },
                        {
                            name: "Grand Oral",
                            data: range(21).map(val => {
                                return { x: val, y: data.filter(s => s.epreuves.grandOral.grade === val).length }
                            }),
                            color: CHART_COLORS[3 % CHART_COLORS.length]
                        },
                        {
                            name: subjectName(student.epreuves.firstOption.name),
                            data: range(21).map(val => {
                                return {
                                    x: val, y: data.filter(s => {
                                        if ((s.epreuves.firstOption.name === student.epreuves.firstOption.name) && (s.epreuves.firstOption.grade === val)) {
                                            return true
                                        } else if ((s.epreuves.secondOption.name === student.epreuves.firstOption.name) && (s.epreuves.secondOption.grade === val)) {
                                            return true
                                        }
                                        return false
                                    }).length
                                }
                            }),
                            color: CHART_COLORS[4 % CHART_COLORS.length]
                        },
                        {
                            name: subjectName(student.epreuves.secondOption.name),
                            data: range(21).map(val => {
                                return {
                                    x: val, y: data.filter(s => {
                                        if ((s.epreuves.firstOption.name === student.epreuves.secondOption.name) && (s.epreuves.firstOption.grade === val)) {
                                            return true
                                        } else if ((s.epreuves.secondOption.name === student.epreuves.secondOption.name) && (s.epreuves.secondOption.grade === val)) {
                                            return true
                                        }
                                        return false
                                    }).length
                                }
                            }),
                            color: CHART_COLORS[5 % CHART_COLORS.length]
                        },
                    ]
                } />
            </div>
        </div>

        <Button
            Icon={IconTrash}
            className="m-10"
            label="Effacer cette personne"
            onClick={() => {
                removeStudent(ine.toString())
            }} />

    </div>
}

export default Student