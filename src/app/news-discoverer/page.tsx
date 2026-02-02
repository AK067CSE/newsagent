"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  ArrowLeft,
  Search,
  Globe,
  TrendingUp,
  Calendar,
  Zap,
  Newspaper,
} from "lucide-react";
import { NewsResponse } from "@/types/NewsResponse";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";
import { API_ENDPOINTS, executeTask } from "@/config/api";

export default function NewsDiscovererPage() {
  const [query, setQuery] = useState("");
  const [daysBack, setDaysBack] = useState(7);
  const [maxArticles, setMaxArticles] = useState(50);
  const [result, setResult] = useState<NewsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const { userId, sessionId } = useSession();

  const loadLastDiscovered = () => {
    try {
      const raw = localStorage.getItem("bynd:last_discovered_articles");
      const arr = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(arr) || arr.length === 0) {
        alert("No discovered articles found yet.");
        return;
      }
      const savedQuery = localStorage.getItem("bynd:last_discovered_query") || "";
      setQuery(savedQuery);
      setResult({
        status: "success",
        articles: arr,
        total_found: arr.length,
        sources_used: [],
        success_rate: "100%",
      } as any);
    } catch (e) {
      console.error(e);
      alert("Failed to load last discovered articles");
    }
  };

  const handleDiscover = async () => {
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        query: query,
        days_back: daysBack,
        max_articles: maxArticles
      };
      
      const data = await executeTask(API_ENDPOINTS.NEWS_DISCOVERER, payload);
      setResult(data);

      try {
        const articles = Array.isArray((data as any)?.articles) ? (data as any).articles : [];
        localStorage.setItem("bynd:last_discovered_articles", JSON.stringify(articles));
        localStorage.setItem("bynd:last_discovered_query", query);
        localStorage.setItem("bynd:last_discovered_at", new Date().toISOString());
      } catch (e) {
        console.warn("Failed to persist discovered articles:", e);
      }
    } catch (err) {
      console.error('Error:', err);
      alert("Failed to discover news: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="mx-auto px-4 py-8 relative z-10">
        <BackgroundBlur />

        {/* Navigation */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/dashboard">
            <Button className="button-secondary flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
          </Link>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Hero section */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
              <Search className="w-4 h-4 mr-2 text-blue-400" />
              <span className="text-sm font-medium text-white/80">
                News Discovery AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Multi-Site News
              <br />
              <span className="gradient-text">Discovery</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Discover news articles from multiple sources using advanced search algorithms 
              and WebRAG technology for comprehensive coverage.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <Globe className="h-6 w-6 text-blue-400" />
                Search Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">
                  Search Query
                </label>
                <input
                  type="text"
                  placeholder="e.g., AI companies, technology news, OpenAI"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-blue-400"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Days Back
                  </label>
                  <select
                    value={daysBack}
                    onChange={(e) => setDaysBack(Number(e.target.value))}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value={1}>Last 24 hours</option>
                    <option value={3}>Last 3 days</option>
                    <option value={7}>Last 7 days</option>
                    <option value={14}>Last 2 weeks</option>
                    <option value={30}>Last month</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Max Articles
                  </label>
                  <select
                    value={maxArticles}
                    onChange={(e) => setMaxArticles(Number(e.target.value))}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value={20}>20 articles</option>
                    <option value={50}>50 articles</option>
                    <option value={100}>100 articles</option>
                    <option value={200}>200 articles</option>
                  </select>
                </div>
              </div>

              <Button
                onClick={handleDiscover}
                disabled={loading || !query}
                className="w-full button-primary flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Discovering News...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    Discover News
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center gap-3">
                    <Newspaper className="h-6 w-6 text-green-400" />
                    Discovery Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.total_found}</div>
                      <div className="text-sm text-white/70">Articles Found</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Calendar className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{daysBack}</div>
                      <div className="text-sm text-white/70">Days Covered</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Globe className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.sources_used?.length || 0}</div>
                      <div className="text-sm text-white/70">Sources</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Zap className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.success_rate || "100%"}</div>
                      <div className="text-sm text-white/70">Success Rate</div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {result.articles?.slice(0, 5).map((article, index) => (
                      <div key={index} className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <h3 className="font-semibold text-white mb-2">{article.title}</h3>
                        <div className="flex items-center gap-4 text-sm text-white/70">
                          <span>{article.source}</span>
                          <span>•</span>
                          <span>{new Date(article.published).toLocaleDateString()}</span>
                        </div>
                        <a 
                          href={article.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block"
                        >
                          Read Article →
                        </a>
                      </div>
                    ))}
                  </div>

                  {result.articles?.length > 5 && (
                    <div className="text-center mt-6">
                      <p className="text-white/70">
                        And {result.articles.length - 5} more articles...
                      </p>
                    </div>
                  )}

                  <div className="mt-8 p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="text-sm font-medium text-white mb-3">Quick Actions</div>
                    <div className="flex flex-wrap gap-2">
                      <Button
                        onClick={loadLastDiscovered}
                        variant="outline"
                        className="text-xs"
                      >
                        Load Last Discovered
                      </Button>
                      <Link href="/content-classifier">
                        <Button variant="outline" className="text-xs">Open Classifier</Button>
                      </Link>
                      <Link href="/data-exporter">
                        <Button variant="outline" className="text-xs">Open Exporter</Button>
                      </Link>
                      <Link href="/web-scraper">
                        <Button variant="outline" className="text-xs">Open WebRAG</Button>
                      </Link>
                      <Link href="/ai-summarizer">
                        <Button variant="outline" className="text-xs">Open Summarizer</Button>
                      </Link>
                    </div>
                    <div className="text-xs text-white/60 mt-2">
                      These pages will automatically use the last discovered articles.
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
