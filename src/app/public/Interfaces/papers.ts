export interface Papers {
  Titles :string,
  Keywords : string,
  Abstract : string
}

export interface PapersResponse{
  weighted_matrix: string;
  titles_matrix: string;
  keywords_matrix: string;
  abstracts_matrix: string;
}