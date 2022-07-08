import _fr from "apexcharts/dist/locales/fr.json";
import dynamic from "next/dynamic";

export const fr = _fr

export const Chart = dynamic(() => import('react-apexcharts'), { ssr: false })