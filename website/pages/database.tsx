import Link from "next/link";
import data from "data/results.json"
import { similar } from "utils/similarity";
import { useEffect } from "react";
import { useState } from "react"

const Database = () => {
    const [search, setSearch] = useState<string>();
    const [elements, setElements] = useState(data);
    const [classes, setClasses] = useState(data.map(v => v.class).filter((value, index, self) => self.indexOf(value) === index))

    useEffect(() => {
        if (!search) {
            setElements(data);
            return
        }
        setElements(similar(data, search, ["lastName", "firstNames.0", "firstNames.1", "firstNames.2", "usageName"]))
    }, [search])

    useEffect(() => {
        setClasses(elements.map(v => v.class).filter((value, index, self) => self.indexOf(value) === index))
    }, [elements])

    data.sort((a, b) => a.lastName.localeCompare(b.lastName))

    return <div className="flex flex-col">
        <div className="w-4/5 self-center">
            <h1 className="text-2xl font-bold mb-2">Base de données</h1>
            <input placeholder="Search..." className="my-3 bg-slate-100 bg-opacity-80 rounded p-2 focus:shadow-lg focus:shadow-slate-200 outline-none transition w-full" type="text" value={search} onChange={t => setSearch(t.target.value)} />
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