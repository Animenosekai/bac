import { useEffect, useState } from "react"

import { FastAverageColor } from "fast-average-color"
import Image from "next/image"
import data from "data/subjects.json"
import twemoji from "twemoji"

const createEmojiURL = (emoji: string) => {
    const img = twemoji.convert.toCodePoint(emoji)
    return `https://twemoji.maxcdn.com/v/latest/svg/${img}.svg`
}

const Twemoji = ({ emoji, size = 72 }) => {
    return <Image
        src={createEmojiURL(emoji)}
        height={size}
        width={size}
        alt={emoji}
    />
}

export const Subject = ({ subject }: { subject: string }) => {
    const [result, setResult] = useState(data[subject] ?? {
        "emoji": "📚",
        "color": console.warn("Couldn't find the subject", subject),
        "short": subject,
        "category": "other"
    });
    const [color, setColor] = useState<{ rgba: string, isDark: boolean }>({
        rgba: "rgba(243, 244, 246, 0.5)",
        isDark: false
    });

    useEffect(() => {
        new FastAverageColor()
            .getColorAsync(createEmojiURL(result.emoji))
            .then(col => {
                setColor(col)
            })
    }, [result])

    useEffect(() => {
        setResult(data[subject] ?? {
            "emoji": "📚",
            "color": console.warn("Couldn't find the subject", subject),
            "short": subject,
            "category": "other"
        })
    }, [subject])

    return <div className="flex flex-col rounded w-max p-4 min-w-[130px]" style={{
        backgroundColor: color.rgba,
        // color: color.isDark ? '#fff' : '#000'
        color: '#000'
    }}>
        <div className="self-center">
            <Twemoji emoji={result.emoji} />
        </div>
        <div className="self-center">
            <span className="font-semibold">{result.short}</span>
        </div>
    </div>
}