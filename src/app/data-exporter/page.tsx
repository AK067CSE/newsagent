"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  ArrowLeft,
  Download,
  FileText,
  CheckCircle,
  Database,
  Save,
} from "lucide-react";
import { ExportResponse } from "@/types/ExportResponse";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";
import { API_BASE_URL, API_ENDPOINTS, executeTask } from "@/config/api";

export default function DataExporterPage() {
  const [articles, setArticles] = useState("");
  const [formatType, setFormatType] = useState("csv");
  const [filename, setFilename] = useState("");
  const [result, setResult] = useState<ExportResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [discovered, setDiscovered] = useState<any[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const { userId, sessionId } = useSession();

  useEffect(() => {
    // Auto-load all last discovered articles by default
    try {
      const raw = localStorage.getItem("bynd:last_discovered_articles");
      const arr = raw ? JSON.parse(raw) : [];
      if (Array.isArray(arr) && arr.length > 0) {
        setDiscovered(arr);
        setSelectedIndex(-1);
        setArticles(JSON.stringify({ articles: arr }, null, 2));
      }
    } catch {
      // ignore
    }
  }, []);

  const handleExport = async () => {
    setLoading(true);
    setResult(null);
    try {
      // Default to exporting all last discovered if textarea is empty
      let parsedArticles: any = null;
      if (!articles.trim()) {
        const raw = localStorage.getItem("bynd:last_discovered_articles");
        const arr = raw ? JSON.parse(raw) : [];
        if (!Array.isArray(arr) || arr.length === 0) {
          alert("No discovered articles found. Run News Discoverer first.");
          return;
        }
        parsedArticles = { articles: arr };
        setDiscovered(arr);
        setSelectedIndex(-1);
        setArticles(JSON.stringify({ articles: arr }, null, 2));
      } else {
        try {
          parsedArticles = JSON.parse(articles);
        } catch (e) {
          alert("Invalid JSON format for articles");
          return;
        }
      }
      
      const payload = {
        articles: parsedArticles,
        format: formatType,
        filename: filename || undefined
      };
      
      const data = await executeTask(API_ENDPOINTS.DATA_EXPORTER, payload);
      setResult(data);
    } catch (err) {
      console.error('Error:', err);
      alert("Failed to export articles: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!result?.download_url) return;
    const url = `${API_BASE_URL}${result.download_url}`;
    window.open(url, "_blank");
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
              <Download className="w-4 h-4 mr-2 text-orange-400" />
              <span className="text-sm font-medium text-white/80">
                Data Exporter AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Professional Data
              <br />
              <span className="gradient-text">Export</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Export processed news articles in multiple formats with proper organization 
              and submission-ready files for your analysis and reporting needs.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <Save className="h-6 w-6 text-orange-400" />
                Export Configuration
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
                      className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-orange-400 text-sm"
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
                  placeholder='{"articles": [{"title": "...", "summary": "...", "companies": [...], "source": "..."}]}'
                  value={articles}
                  onChange={(e) => setArticles(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-orange-400 font-mono text-sm"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Export Format
                  </label>
                  <select
                    value={formatType}
                    onChange={(e) => setFormatType(e.target.value)}
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-orange-400"
                  >
                    <option value="csv">CSV (Spreadsheet)</option>
                    <option value="json">JSON (Data)</option>
                    <option value="pdf">PDF (Report)</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">
                    Filename (optional)
                  </label>
                  <input
                    type="text"
                    value={filename}
                    onChange={(e) => setFilename(e.target.value)}
                    placeholder="financial_news"
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:border-orange-400"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                {[
                  { format: "csv", desc: "Excel compatible", icon: Database },
                  { format: "json", desc: "API ready", icon: FileText },
                  { format: "pdf", desc: "Printable report", icon: Save }
                ].map((option) => (
                  <button
                    key={option.format}
                    onClick={() => setFormatType(option.format)}
                    className={`p-3 rounded-lg border transition-all ${
                      formatType === option.format
                        ? "bg-orange-500/20 border-orange-400 text-white"
                        : "bg-white/5 border-white/20 text-white/70 hover:bg-white/10"
                    }`}
                  >
                    <option.icon className="h-5 w-5 mx-auto mb-1" />
                    <div className="font-medium text-sm">{option.format.toUpperCase()}</div>
                    <div className="text-xs opacity-70">{option.desc}</div>
                  </button>
                ))}
              </div>

              <Button
                onClick={handleExport}
                disabled={loading || !articles}
                className="w-full button-primary flex items-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Exporting Data...
                  </>
                ) : (
                  <>
                    <Download className="h-4 w-4" />
                    Export Data
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
                    Export Results
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <FileText className="h-8 w-8 text-blue-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.exported_count}</div>
                      <div className="text-sm text-white/70">Articles Exported</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Database className="h-8 w-8 text-green-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.format?.toUpperCase()}</div>
                      <div className="text-sm text-white/70">Format</div>
                    </div>
                    <div className="text-center p-4 bg-white/5 rounded-lg">
                      <Save className="h-8 w-8 text-orange-400 mx-auto mb-2" />
                      <div className="text-2xl font-bold text-white">{result.filename || ""}</div>
                      <div className="text-sm text-white/70">File</div>
                    </div>
                  </div>

                  <div className="p-4 bg-green-500/10 border border-green-400/20 rounded-lg mb-6">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="h-4 w-4 text-green-400" />
                      <span className="text-sm font-medium text-green-300">Export Successful</span>
                    </div>
                    <p className="text-sm text-green-200">
                      {result.message}
                    </p>
                  </div>

                  {result.download_url && (
                    <Button
                      onClick={handleDownload}
                      className="w-full button-primary flex items-center gap-2"
                    >
                      <Download className="h-4 w-4" />
                      Download {result.format?.toUpperCase()}
                    </Button>
                  )}

                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
