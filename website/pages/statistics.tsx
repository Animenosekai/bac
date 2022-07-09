import { Card } from "components/cards/card";
import { Chart } from "components/chart";
import { Section } from "components/cards/section";
import { useData } from "contexts/data"

const CHART_COLORS = ["#008FFB"]

const Statistics = () => {
    const { data } = useData();

    const classes = data.map(val => val.class).filter((value, index, self) => self.indexOf(value) === index)

    return <div>
        <Section title="Mentions">
            <Card>
                <Chart height={400} type="bar" options={{
                    chart: {
                        stacked: true,
                        toolbar: { show: true },
                        zoom: { enabled: true }
                    },
                    responsive: [{
                        breakpoint: 480,
                        options: {
                            legend: {
                                position: 'bottom',
                                offsetX: -10,
                                offsetY: 0
                            }
                        }
                    }],
                    plotOptions: {
                        bar: {
                            horizontal: false,
                            borderRadius: 10
                        },
                    },
                    xaxis: {
                        type: 'category',
                        categories: ["Sans Mention", "Assez Bien", "Bien", "Très Bien", "Félicitations du Jury"],
                    },
                    legend: {
                        position: 'right',
                        offsetY: 40
                    },
                    annotations: {
                        xaxis: [
                            {
                                x: "Sans Mention",
                                borderColor: "transparent",
                                label: {
                                    borderColor: "#008FFB",
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: "#008FFB"
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: `${Math.round((data.filter(val => !val.mention).length / data.length) * 10000) / 100}%`
                                }
                            },
                            {
                                x: "Assez Bien",
                                borderColor: "transparent",
                                label: {
                                    borderColor: "#008FFB",
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: "#008FFB"
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: `${Math.round((data.filter(val => val.mention && val.mention?.startsWith("Assez")).length / data.length)* 10000) / 100}%`
                                }
                            },
                            {
                                x: "Bien",
                                borderColor: "transparent",
                                label: {
                                    borderColor: "#008FFB",
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: "#008FFB"
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: `${Math.round((data.filter(val => val.mention && val.mention === "Bien").length / data.length) * 10000) / 100}%`
                                }
                            },
                            {
                                x: "Très Bien",
                                borderColor: "transparent",
                                label: {
                                    borderColor: "#008FFB",
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: "#008FFB"
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: `${Math.round((data.filter(val => val.mention && val.mention === "Très Bien").length / data.length) * 10000) / 100}%`
                                }
                            },
                            {
                                x: "Félicitations du Jury",
                                borderColor: "transparent",
                                label: {
                                    borderColor: "#008FFB",
                                    style: {
                                        fontSize: '12px',
                                        color: '#fff',
                                        background: "#008FFB"
                                    },
                                    orientation: 'horizontal',
                                    offsetY: 7,
                                    text: `${Math.round((data.filter(val => val.mention && val.mention.toLowerCase().endsWith("jury")).length / data.length) * 10000) / 100}%`
                                }
                            }
                        ]
                    },
                    fill: { opacity: 1 }
                }} series={
                    classes.map(currentClass => {
                        const results = [0, 0, 0, 0, 0]
                        data.filter(student => student.class === currentClass).forEach(student => {
                            if (!student.mention) {
                                results[0] += 1
                            } else if (student.mention.startsWith("Assez")) {
                                results[1] += 1
                            } else if (student.mention === "Bien") {
                                results[2] += 1
                            } else if (student.mention === "Très Bien") {
                                results[3] += 1
                            } else if (student.mention.toLowerCase().endsWith("jury")) {
                                results[4] += 1
                            }
                        })
                        return { name: currentClass, data: results }
                    })} />
            </Card>
        </Section>
    </div>
}
export default Statistics