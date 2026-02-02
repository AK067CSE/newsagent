export interface ClassificationResponse {
  status: string;
  articles: ClassifiedArticle[];
  total_relevant: number;
  total_input: number;
  companies_targeted: string[];
}

export interface ClassifiedArticle {
  title: string;
  url: string;
  published: string;
  source: string;
  content?: string;
  companies: string[];
  summary?: string;
}
