export interface NewsResponse {
  status: string;
  articles: NewsArticle[];
  total_found: number;
  sources_used?: string[];
  success_rate?: string;
}

export interface NewsArticle {
  title: string;
  url: string;
  published: string;
  source: string;
  content?: string;
  companies?: string[];
  summary?: string;
  scraping_method?: string;
  scraped_at?: string;
}
