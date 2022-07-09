import { HTMLAttributes } from "react"

export const Card = ({ children, ...props }: HTMLAttributes<HTMLDivElement>) => {
    return <div className='flex flex-col bg-gray-100 rounded-lg bg-opacity-80 p-5 m-5 self-center w-4/5 min-w-max'>{children}</div>
}