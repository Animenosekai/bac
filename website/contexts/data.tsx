import React, { createContext, useContext, useEffect, useState } from "react";

import { Results } from "lib/results";
import localforage from "localforage";

export const DataStore = localforage.createInstance({
    name: "bac-data",
    storeName: "bacdata",
    description: "This stores the parsed data to be used on the website"
})

export const DataContext = createContext<{
    data: Results
    clearData: () => void;
    mergeData: (newData: Results) => void;
    removeStudent: (ine: string) => void;
}>(undefined);

export const useData = () => useContext(DataContext);

export const DataContextConsumer = DataContext.Consumer;

export interface DataContextProps {
    children
}

export const DataContextProvider = ({ children }: DataContextProps) => {
    const [data, setData] = useState<Results>([]);

    useEffect(() => {
        DataStore.setItem("data", data)
    }, [data])

    useEffect(() => {
        DataStore.getItem("data")
            .then((val: Results) => {
                if (val) {
                    mergeData(val)
                } else {
                    console.warn("No data found")
                }
            })
    }, [])

    const clearData = () => {
        setData([])
    }

    const removeStudent = (ine: string) => {
        setData(data => {
            return data.filter(val => val.ine !== ine)
        })
    }

    const mergeData = (newData: Results) => {
        if (!newData) { return }
        setData(data => {
            const INE = data.map(val => val.ine)
            const result = newData.filter(val => !INE.includes(val.ine))
            return [...data, ...result]
        })
    }


    // SETTING THE VALUES
    return <DataContext.Provider value={{
        data,
        clearData,
        mergeData,
        removeStudent
    }}>
        {children}
    </DataContext.Provider>
}