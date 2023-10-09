export interface HeatMap {
    xaxis: Xaxis[]
    yaxis: Yaxis[]
    data: HeatMapData[]
}

export interface HeatMapData {
    yaxis: string
    xaxis: string
    value: number
}

export interface Yaxis {
    yaxis:string
}

export interface Xaxis {
    xaxis:string
}