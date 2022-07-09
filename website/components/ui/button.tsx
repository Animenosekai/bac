import { HTMLAttributes } from "react"
import { TablerIcon } from "@tabler/icons"
import classNames from "classnames"

export interface ButtonProps extends HTMLAttributes<HTMLButtonElement> {
    Icon?: TablerIcon
    label?: string
}

export const Button = ({ onClick, className, Icon, label, ...props }: ButtonProps) => {
    return <button
        className={classNames("py-2 px-4 hover:text-black hover:bg-white transition bg-black border-[1px] border-black text-white rounded-md w-fit h-min", className)}
        onClick={onClick}
        {...props}
    >
        <div className="flex space-x-2">
            {Icon && <Icon strokeWidth="1.25" />}
            {label && <span>{label}</span>}
        </div>
    </button>
}
