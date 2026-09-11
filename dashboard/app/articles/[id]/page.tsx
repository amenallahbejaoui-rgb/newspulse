"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

const API = "http://127.0.0.1:8000";

type Article = {
  id: number;
  title: string;
  url: string;
  summary: string | null;
  content: string | null;
  published: string | null;
  source: string;
  category: string;
  content_type: string;
};

export default function ArticlePage() {
  const params = useParams();
  const id = params.id;

  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadArticle() {
      try {
        const response = await fetch(`${API}/articles/${id}`);
        const data = await response.json();

        if (!data.error) {
          setArticle(data);
        }
      } catch (error) {
        console.error("Failed to load article:", error);
      } finally {
        setLoading(false);
      }
    }

    if (id) {
      loadArticle();
    }
  }, [id]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-100">
        <p className="text-gray-500">Loading article...</p>
      </main>
    );
  }

  if (!article) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-100">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Article not found</h1>

          <Link
            href="/"
            className="mt-4 inline-block text-blue-600 hover:underline"
          >
            ← Back to NewsPulse
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-4xl px-6 py-5">
          <Link
            href="/"
            className="text-sm font-medium text-blue-600 hover:underline"
          >
            ← Back to NewsPulse
          </Link>
        </div>
      </header>

      <article className="mx-auto max-w-4xl px-6 py-10">
        <div className="rounded-2xl border bg-white p-8 shadow-sm">
          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-3 text-sm">
            <span className="rounded-full bg-gray-100 px-3 py-1 font-medium">
              {article.category}
            </span>

            <span className="text-gray-500">
              {article.source}
            </span>

            <span className="text-gray-400">
              {article.content_type}
            </span>
          </div>

          {/* Title */}
          <h1 className="mt-6 text-3xl font-bold leading-tight text-gray-900 md:text-4xl">
            {article.title}
          </h1>

          {/* Published */}
          {article.published && (
            <p className="mt-4 text-sm text-gray-500">
              Published: {article.published}
            </p>
          )}

          {/* Summary */}
          {article.summary && (
            <div className="mt-8 rounded-xl bg-gray-50 p-5">
              <p className="text-base leading-7 text-gray-700">
                {article.summary}
              </p>
            </div>
          )}

          {/* Content */}
          {article.content_type === "video" ? (
            <div className="mt-8 rounded-xl bg-gray-50 p-8 text-center">
              <p className="text-gray-600">
                This is a video item.
              </p>

              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-block rounded-lg bg-black px-5 py-2 text-sm font-medium text-white"
              >
                Watch original →
              </a>
            </div>
          ) : (
            <div className="mt-8">
              {article.content ? (
                article.content.split("\n\n").map((paragraph, index) => (
                  <p
                    key={index}
                    className="mb-6 text-lg leading-8 text-gray-800"
                  >
                    {paragraph}
                  </p>
                ))
              ) : (
                <p className="text-gray-500">
                  Full article content is not available.
                </p>
              )}
            </div>
          )}

          {/* Original */}
          <div className="mt-10 border-t pt-6">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex rounded-lg bg-black px-5 py-3 text-sm font-medium text-white hover:bg-gray-800"
            >
              Read original article →
            </a>
          </div>
        </div>
      </article>
    </main>
  );
}