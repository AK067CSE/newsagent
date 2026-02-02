export interface SummarizationResponse {
  status: string;
  articles: SummarizedArticle[];
  total_summarized: number;
  format: string;
}

export interface SummarizedArticle {
  title: string;
  url: string;
  published: string;
  source: string;
  content?: string;
  companies?: string[];
  summary: string;
  word_count?: number;
}
