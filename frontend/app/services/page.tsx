"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  Briefcase,
  GraduationCap,
  HeartPulse,
  Home,
  Landmark,
  Search,
  Users,
} from "lucide-react";
import { getSchemes, type Scheme } from "../../lib/api";

const categoryIcons = [GraduationCap, HeartPulse, Home, Briefcase, Landmark, Users];

function getCategoryIcon(category: string) {
  return categoryIcons[category.length % categoryIcons.length];
}

export default function ServicesPage() {
  const [search, setSearch] = useState("");
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const loadSchemes = async () => {
      setIsLoading(true);
      try {
        const result = await getSchemes(search.trim() || undefined);
        if (!cancelled) {
          setSchemes(result);
          setError(null);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError instanceof Error ? requestError.message : "Unable to load government schemes.");
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    const timer = window.setTimeout(loadSchemes, 250);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [search]);

  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2 font-semibold text-slate-900">
            <ArrowLeft size={20} />
            Back to Home
          </Link>
          <div className="font-bold text-blue-600">Citizen AI</div>
        </div>
      </header>

      <section className="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-16 text-white">
        <div className="mx-auto max-w-6xl">
          <p className="mb-3 font-medium text-blue-100">Government Services</p>
          <h1 className="text-4xl font-bold md:text-5xl">Find Services Made for You</h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-blue-100">
            Search live scheme information from the NagrikSetu backend.
          </p>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-8">
        <div className="flex items-center gap-3 rounded-2xl border bg-white px-4 py-3 shadow-sm">
          <Search size={22} className="text-slate-400" />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            type="search"
            placeholder="Search government schemes..."
            className="w-full bg-transparent text-slate-900 outline-none placeholder:text-slate-400"
            aria-label="Search government schemes"
          />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-16">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900">Available Schemes</h2>
          <p className="mt-2 text-slate-600">{schemes.length} schemes matched your search.</p>
        </div>

        {isLoading && <p className="text-slate-600">Loading schemes...</p>}
        {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</p>}
        {!isLoading && !error && schemes.length === 0 && (
          <p className="rounded-xl border bg-white p-6 text-slate-600">No schemes matched that search.</p>
        )}

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {schemes.map((scheme) => {
            const Icon = getCategoryIcon(scheme.category);
            return (
              <article key={scheme.id} className="rounded-2xl border bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-blue-600">
                  <Icon size={25} />
                </div>
                <p className="mb-2 text-sm font-medium text-blue-600">{scheme.category}</p>
                <h3 className="text-xl font-bold text-slate-900">{scheme.title}</h3>
                <p className="mt-3 leading-7 text-slate-600">{scheme.short_description}</p>
                <p className="mt-3 text-xs text-slate-500">{scheme.department} · {scheme.level}</p>
                <div className="mt-6 flex items-center gap-4">
                  <Link href={`/chat?scheme=${scheme.id}`} className="font-semibold text-blue-600 hover:text-blue-700">
                    Ask Citizen AI
                  </Link>
                  {scheme.application_url && (
                    <a href={scheme.application_url} target="_blank" rel="noreferrer" className="text-sm font-semibold text-slate-600 hover:text-slate-900">
                      Official portal
                    </a>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </main>
  );
}
