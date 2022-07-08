import Link from "next/link"
import { range } from "utils/range"

export const Rank = ({ data, selected, selectedRank, increment }: { data: { id: string, name: string, link?: string }[], selected: string, selectedRank: number, increment?: number }) => {
    const index = data.findIndex(val => val.id === selected)
    return <div>
        <ol className="space-y-2">
            {
                range(data.length, -index).map((val, i) => {
                    return <li key={i}>
                        <Link href={data[val + index].link} passHref={true}>
                            <a>
                                <div style={{
                                    opacity: 1 - ((val > 0 ? val : -val) / (10 / increment ?? 2)),
                                    display: (1 - ((val > 0 ? val : -val) / (10 / increment ?? 2))) <= 0 ? "none" : "flex",
                                    fontSize: 20 - ((val > 0 ? val : -val) * (2 / increment ?? 2))
                                }} className="bg-gray-200 py-2 px-4 rounded justify-between">
                                    <span>{data[val + index].name}</span>
                                    <span>#{selectedRank + val + 1}</span>
                                </div>
                            </a>
                        </Link>
                    </li>
                })
            }
        </ol>
    </div>
}