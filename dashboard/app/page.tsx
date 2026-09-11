"use client";

import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

type Article = {
  id: number;
  title: string;
  url: string;
  summary: string | null;
  published: string | null;
  source: string;
  category: string;
  content_type: string;
};

type Stats = {
  total: number;
  articles: number;
  videos: number;
  categories: number;
};

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [articles, setArticles] = useState<Article[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [sources, setSources] = useState<string[]>([]);

  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [source, setSource] = useState("");

  const [loading, setLoading] = useState(true);

  async function loadDashboard() {
    setLoading(true);

    try {
      const params = new URLSearchParams();

      params.set("page", String(page));
      params.set("limit", "12");

      if (search) {
        params.set("search", search);
      }

      if (category) {
        params.set("category", category);
      }

      if (source) {
        params.set("source", source);
      }

      const [statsRes, articlesRes, categoriesRes, sourcesRes] =
        await Promise.all([
          fetch(`${API}/stats`),
          fetch(`${API}/articles?${params.toString()}`),
          fetch(`${API}/categories`),
          fetch(`${API}/sources`),
        ]);

      const statsData = await statsRes.json();
      const articlesData = await articlesRes.json();
      const categoriesData = await categoriesRes.json();
      const sourcesData = await sourcesRes.json();

      setStats(statsData);
      setArticles(articlesData.articles);
      setPages(articlesData.pages);
      setCategories(categoriesData.categories);
      setSources(sourcesData.sources);
    } catch (error) {
      console.error("Failed to load dashboard:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
  }, [page]);

  function handleSearch() {
    setPage(1);

    if (page === 1) {
      void loadDashboard();
    }
  }

  function handleRefresh() {
    void loadDashboard();
  }

  function handleNextPage() {
    if (page < pages) {
      setPage((current) => current + 1);
    }
  }

  function handlePreviousPage() {
    if (page > 1) {
      setPage((current) => current - 1);
    }
  }

  return (
    <main className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              NewsPulse
            </h1>

            <p className="text-sm text-gray-500">
              News aggregation dashboard
            </p>
          </div>

          <button
            onClick={handleRefresh}
            className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
          >
            Refresh
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* Stats */}
        <div className="grid gap-4 md:grid-cols-4">
          <StatCard
            title="Total"
            value={stats?.total ?? 0}
          />

          <StatCard
            title="Articles"
            value={stats?.articles ?? 0}
          />

          <StatCard
            title="Videos"
            value={stats?.videos ?? 0}
          />

          <StatCard
            title="Categories"
            value={stats?.categories ?? 0}
          />
        </div>

        {/* Filters */}
        <div className="mt-8 rounded-xl border bg-white p-5">
          <div className="grid gap-4 md:grid-cols-4">
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSearch();
                }
              }}
              placeholder="Search articles..."
              className="rounded-lg border px-4 py-2 text-sm outline-none focus:border-black"
            />

            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
              }}
              className="rounded-lg border px-4 py-2 text-sm"
            >
              <option value="">All categories</option>

              {categories.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <select
              value={source}
              onChange={(e) => {
                setSource(e.target.value);
              }}
              className="rounded-lg border px-4 py-2 text-sm"
            >
              <option value="">All sources</option>

              {sources.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <button
              onClick={handleSearch}
              className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
            >
              Apply filters
            </button>
          </div>
        </div>

        {/* Articles */}
        <div className="mt-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">
              Latest news
            </h2>

            <span className="text-sm text-gray-500">
              {articles.length} results
            </span>
          </div>

          {loading ? (
            <div className="rounded-xl border bg-white p-10 text-center text-gray-500">
              Loading news...
            </div>
          ) : articles.length === 0 ? (
            <div className="rounded-xl border bg-white p-10 text-center text-gray-500">
              No articles found.
            </div>
          ) : (
            <>
              {/* Article Cards */}
              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {articles.map((article) => (
                  <ArticleCard
                    key={article.id}
                    article={article}
                  />
                ))}
              </div>

              {/* Pagination */}
              <div className="mt-8 flex items-center justify-center gap-4">
                <button
                  onClick={handlePreviousPage}
                  disabled={page === 1}
                  className="rounded-lg border bg-white px-4 py-2 text-sm font-medium hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  ← Previous
                </button>

                <span className="text-sm text-gray-600">
                  Page {page} of {pages}
                </span>

                <button
                  onClick={handleNextPage}
                  disabled={page === pages}
                  className="rounded-lg border bg-white px-4 py-2 text-sm font-medium hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Next →
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}

function StatCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border bg-white p-5">
      <p className="text-sm text-gray-500">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold text-gray-900">
        {value}
      </p>
    </div>
  );
}

function ArticleCard({
  article,
}: {
  article: Article;
}) {
  return (
    <article className="flex h-full flex-col rounded-xl border bg-white p-5 shadow-sm">
      <div className="flex items-center gap-2 text-xs">
        <span className="rounded-full bg-gray-100 px-2 py-1 font-medium">
          {article.category}
        </span>

        <span className="text-gray-500">
          {article.content_type}
        </span>
      </div>

      <a
        href={`/articles/${article.id}`}
        className="mt-4 line-clamp-3 text-lg font-semibold text-gray-900 hover:underline"
      >
        {article.title}
      </a>

      {article.summary && (
        <p className="mt-3 line-clamp-3 text-sm leading-6 text-gray-600">
          {article.summary}
        </p>
      )}

      <div className="mt-auto pt-5">
        <div className="mb-3 text-xs text-gray-500">
          {article.source}
        </div>

        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium text-blue-600 hover:underline"
        >
          Read original article →
        </a>
      </div>
    </article>
  );
}

