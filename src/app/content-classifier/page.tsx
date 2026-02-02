"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  ArrowLeft,
  Tags,
  Building,
  Filter,
  CheckCircle,
  AlertCircle,
  TrendingUp,
} from "lucide-react";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";
import { apiCall, API_ENDPOINTS } from "@/config/api";

type ClassifyApiResponse = {
  status: string;
  by_company: Record<string, any[]>;
  unclassified: any[];
};

export default function ContentClassifierPage() {
  const [articles, setArticles] = useState("");
  const [companySet, setCompanySet] = useState("OpenAI,Anthropic,Google DeepMind,Microsoft,Meta");
  const [result, setResult] = useState<ClassifyApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [discovered, setDiscovered] = useState<any[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const { userId, sessionId } = useSession();

  const handleClassify = async () => {
    setLoading(true);
    setResult(null);
    try {
      // Parse articles from textarea
      let parsedArticles: any = [];
      try {
        parsedArticles = JSON.parse(articles);
      } catch (e) {
        alert("Invalid JSON format for articles");
        return;
      }

      const normalizedArticles = Array.isArray(parsedArticles)
        ? parsedArticles
        : Array.isArray(parsedArticles?.articles)
        ? parsedArticles.articles
        : [];
      
      const payload = {
        articles: normalizedArticles,
        companies: companySet.split(',').map(c => c.trim()).filter(Boolean)
      };

      const data = await apiCall(API_ENDPOINTS.CLASSIFY, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setResult(data as ClassifyApiResponse);
    } catch (err) {
      console.error('Error:', err);
      alert("Failed to classify articles: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const loadFromDiscoverer = () => {
    try {
      const raw = localStorage.getItem("bynd:last_discovered_articles");
      const arr = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(arr) || arr.length === 0) {
        alert("No discovered articles found. Run News Discoverer first.");
        return;
      }
      setDiscovered(arr);
      setSelectedIndex(-1);
      setArticles(JSON.stringify({ articles: arr }, null, 2));
    } catch (e) {
      console.error(e);
      alert("Failed to load discovered articles");
    }
  };

  const loadSelectedDiscovered = (idx: number) => {
    setSelectedIndex(idx);
    if (idx < 0) {
      setArticles(JSON.stringify({ articles: discovered }, null, 2));
      return;
    }
    const one = discovered[idx];
    setArticles(JSON.stringify({ articles: one ? [one] : [] }, null, 2));
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
              <Tags className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-white/80">
                Content Classifier AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Entity
              <br />
              <span className="gradient-text">Classification</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Classify and tag news articles by company entities using advanced NLP 
              techniques for accurate content categorization and filtering.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <Filter className="h-6 w-6 text-purple-400" />
                Classification Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-white/80">
                    Articles JSON
                  </label>
                  <Button
                    onClick={loadFromDiscoverer}
                    variant="outline"
                    size="sm"
                    className="text-xs"
                  >
                    Load from News Discoverer
                  </Button>
                </div>

                {discovered.length > 0 && (
                  <div className="mb-2">
                    <label className="block text-xs font-medium text-white/70 mb-1">
                      Select discovered article (optional)
                    </label>
                    <select
                      value={selectedIndex}
                      onChange={(e) => loadSelectedDiscovered(Number(e.target.value))}
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-400 text-sm"
                    >
                      <option value={-1}>All discovered articles ({discovered.length})</option>
                      {discovered.slice(0, 50).map((a, idx) => (
                        <option key={idx} value={idx}>
                          {(a?.title || a?.url || "(article)").toString().slice(0, 80)}
                        </option>
                      ))}
                    </select>
                  </div>
                )}
                <textarea
                  placeholder='{"articles": [{"title": "...", "content": "...", "source": "..."}]}'
                  value={articles}
                  onChange={(e) => setArticles(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-purple-400 font-mono text-sm"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">
                  Target Companies (comma-separated)
                </label>
                <input
                  type="text"
                  value={companySet}
                  onChange={(e) => setCompanySet(e.target.value)}
                  placeholder="OpenAI, Anthropic, Microsoft, Google, Meta"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-purple-400"
                />
              </div>

              <Button
                onClick={handleClassify}
                disabled={loading || !articles}
                className="w-full button-primary flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Classifying Content...
                  </>
                ) : (
                  <>
                    <Tags className="h-4 w-4" />
                    Start Classification
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
                    <CheckCircle className="h-6 w-6 text-green-400" />
                    Classification Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {(() => {
                    const byCompany = result.by_company || {};
                    const companies = Object.keys(byCompany);
                    const totalRelevant = companies.reduce((sum, c) => sum + (byCompany[c]?.length || 0), 0);
                    const totalInput = (() => {
                      try {
                        const parsed = JSON.parse(articles);
                        const arr = Array.isArray(parsed) ? parsed : parsed?.articles;
                        return Array.isArray(arr) ? arr.length : 0;
                      } catch {
                        return 0;
                      }
                    })();
                    const matchRate = totalInput ? Math.round((totalRelevant / totalInput) * 100) : 0;
                    const targeted = companySet.split(',').map(c => c.trim()).filter(Boolean);
                    return (
                      <>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Filter className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{totalRelevant}</div>
                      <div className="text-sm text-white/70">Relevant Articles</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <AlertCircle className="h-8 w-8 text-yellow-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">
                        {targeted.length}
                      </div>
                      <div className="text-sm text-white/70">Companies Targeted</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <TrendingUp className="h-8 w-8 text-green-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">
                        {matchRate}%
                      </div>
                      <div className="text-sm text-white/70">Match Rate</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Building className="h-8 w-8 text-purple-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">
                        {result.unclassified?.length || 0}
                      </div>
                      <div className="text-sm text-white/70">Unclassified</div>
                    </div>
                  </div>

                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-white mb-3">Target Companies</h3>
                    <div className="flex flex-wrap gap-2">
                      {targeted.map((company, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-purple-500/20 border border-purple-400 rounded-full text-sm text-purple-300"
                        >
                          {company}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-4">
                    {companies.filter((c) => (byCompany[c]?.length || 0) > 0).map((company) => (
                      <div key={company} className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-white">{company}</h3>
                          <span className="text-sm text-white/70">{byCompany[company]?.length || 0}</span>
                        </div>
                        <div className="text-sm text-white/70">
                          {byCompany[company]?.slice(0, 3).map((a: any, idx: number) => (
                            <div key={idx} className="truncate">{a.title || a.url || "(item)"}</div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {(result.unclassified?.length || 0) > 0 && (
                    <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-400/20 rounded-lg">
                      <div className="text-sm font-medium text-yellow-300 mb-2">Unclassified</div>
                      <div className="text-xs text-yellow-200">
                        {result.unclassified.length} item(s) did not match any company.
                      </div>
                    </div>
                  )}
                      </>
                    );
                  })()}
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
