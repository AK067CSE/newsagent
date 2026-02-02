export interface ScrapingResponse {
  status: string;
  articles: ScrapedArticle[];
  total_scraped: number;
  success_rate: string;
  methods_used: string[];
}

export interface ScrapedArticle {
  title: string;
  url: string;
  published: string;
  source: string;
  content: string;
  scraping_method: string;
  scraped_at: string;
  companies?: string[];
  summary?: string;
}
