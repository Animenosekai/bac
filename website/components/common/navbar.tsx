import Link from "next/link";
import cn from "classnames"

export interface NavbarProps {
    className?: string
}

const NavbarLink = ({ href, name }: { href: string, name: string }) => {
    return <li className="mx-4 opacity-60 hover:opacity-100 transition">
        <Link passHref={true} href={href}>
            <a>{name}</a>
        </Link>
    </li>
}

export const Navbar = ({ className, props }: any) => {
    return <ul className={cn("flex flex-row absolute right-10", className)} {...props}>
        <NavbarLink href="/ranking" name="Ranking" />
        <NavbarLink href="/statistics" name="Statistiques" />
        <NavbarLink href="/database" name="Database" />
    </ul>
}