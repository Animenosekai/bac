import { Subject } from "components/cards/subject"

export const Options = ({ title, options }: { title: string, options: string[] }) => {
    return <div className="flex flex-col space-y-4 rounded py-4 px-6 border-gray-100 border-opacity-50 border-4 shadow-lg hover:shadow-xl transition duration-300">
        <h2 className="text-xl font-medium">{title}</h2>
        <div className="flex flex-row self-center space-x-5 justify-around min-w-max w-full">
            {
                options.map((val, i) => <Subject key={i} subject={val} />)
            }
        </div>
    </div>
}