import { HTMLAttributes } from "react"

export interface SectionProps extends HTMLAttributes<HTMLDivElement> {
    title: string
}

export const Section = ({ title, children, ...props }: SectionProps) => {
    return <div className="m-10 flex flex-col space-y-10" {...props}>
        <h1 className="text-2xl font-semibold">{title}</h1>
        <div className="w-full flex flex-col">
            {children}
        </div>
    </div>
}