import { IconApps, IconFileExport, IconLoader, IconWreckingBall } from "@tabler/icons";

import { Button } from "components/ui/button";
import Configuration from "configuration";
import Link from "next/link";
import { similar } from "utils/similarity";
import { useData } from "contexts/data";
import { useEffect } from "react";
import { useState } from "react"

const Database = () => {
    const [search, setSearch] = useState<string>();
    const { data, clearData, mergeData } = useData();
    const [elements, setElements] = useState(data);
    const [analyze, setAnalyze] = useState("Analyse en cours")
    const [currentAnalyze, setCurrentAnalyze] = useState(false);
    const [classes, setClasses] = useState(data.map(v => v.class).filter((value, index, self) => self.indexOf(value) === index))

    useEffect(() => {
        if (!search) {
            setElements(data);
            return
        }
        setElements(similar(data, search, ["lastName", "firstNames.0", "firstNames.1", "firstNames.2", "usageName"]))
    }, [search, data])

    useEffect(() => {
        setClasses(elements.map(v => v.class).filter((value, index, self) => self.indexOf(value) === index))
    }, [elements])

    useEffect(() => {
        const interval = setInterval(() => {
            setAnalyze(current => {
                if (current.endsWith("...")) {
                    return "Analyse en cours"
                }
                return current + "."
            })
        }, 1000)
        return () => {
            clearInterval(interval)
        }
    }, [])

    data.sort((a, b) => a.lastName.localeCompare(b.lastName))

    return <div className="flex flex-col">
        <div className="w-4/5 self-center">
            <div className="flex flex-col">
                <div className="flex flex-row space-x-2 space-y-2 self-end flex-wrap mb-4">
                    <Button
                        Icon={IconFileExport}
                        label="Exporter les données"
                        className="self-end"
                        onClick={() => {
                            const newElem = document.createElement('a');
                            newElem.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data)));
                            newElem.setAttribute('download', String(new Date().getTime()) + ".anise.json");

                            newElem.style.display = 'none';
                            document.body.appendChild(newElem);
                            newElem.click();
                            document.body.removeChild(newElem);
                        }}
                    />
                    <Button
                        Icon={IconLoader}
                        label="Effacer cette personne"
                        onClick={clearData} />
                    <Button
                        Icon={
                            currentAnalyze
                                ? IconWreckingBall
                                : IconApps
                        }
                        label={
                            currentAnalyze
                                ? analyze
                                : "Importer des données"
                        }
                        onClick={() => {
                            if (currentAnalyze) {
                                return
                            }
                            const newElem = document.createElement("input")
                            newElem.type = "file"
                            newElem.accept = "application/pdf, application/json"
                            newElem.onchange = () => {
                                if (!newElem.files[0]) { return console.warn("The user seems to have aborted the action") }
                                setCurrentAnalyze(true)
                                if (newElem.files[0].name.endsWith(".anise.json")) {
                                    newElem.files[0].text()
                                        .then(val => {
                                            const results = JSON.parse(val)
                                            setCurrentAnalyze(false)
                                            mergeData(results)
                                        })
                                } else {
                                    const formData = new FormData();
                                    formData.append("data", newElem.files[0])
                                    fetch(Configuration.request.host + "/api/parser", {
                                        method: "POST",
                                        body: formData
                                    })
                                        .then(resp => resp.json())
                                        .then(val => {
                                            if (val.success) {
                                                mergeData(val.data.content)
                                            } else {
                                                throw TypeError(`An error occured when parsing the data: ${val.error}`)
                                            }
                                            setCurrentAnalyze(false)
                                        })
                                        .catch((e) => {
                                            console.warn("An error occured when parsing the data", e)
                                            setCurrentAnalyze(false)
                                        })
                                }
                            }
                            newElem.click()
                        }} />
                </div>
                <h1 className="text-2xl font-bold mb-2">Base de données</h1>
                <input placeholder="Search..." className="my-3 bg-slate-100 bg-opacity-80 rounded p-2 focus:shadow-lg focus:shadow-slate-200 outline-none transition w-full" type="text" value={search} onChange={t => setSearch(t.target.value)} />
            </div>
            {
                classes.map((currentClass, i) => {
                    return <div key={i}>
                        <h2 className="text-xl font-medium mt-4 mb-2">{currentClass}</h2>
                        <ul>
                            {
                                elements.filter(v => v.class === currentClass).map((student, k) => {
                                    return <li key={k}>
                                        <Link href={`/database/student/${student.ine}`} passHref={true}>
                                            <a>
                                                <div className="flex flex-row items-center p-3 my-1 bg-gray-100 bg-opacity-75 rounded hover:shadow-md hover:shadow-gray-200 transition justify-between">
                                                    <div className="flex flex-row items-center">
                                                        <span className="text-lg font-medium mr-1">{student.lastName} {student.firstNames[0]}</span>
                                                        {
                                                            student.firstNames.length > 0 && <div className="mx-1">{' '}<span className="text-gray-500 font-medium">{student.firstNames.slice(1).join(" ")}</span></div>
                                                        }
                                                    </div>
                                                    <span className="opacity-50">{student.calculResultat.average} {student.mention && `(${student.mention})`}</span>
                                                </div>
                                            </a>
                                        </Link>
                                    </li>
                                })
                            }
                        </ul>
                    </div>
                })
            }
        </div>
    </div>
}

export default Database