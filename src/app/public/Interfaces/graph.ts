export interface Graph {
    name: string
    value: number
    children: Graph[] | []
}