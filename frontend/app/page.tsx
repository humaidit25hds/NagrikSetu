import Link from "next/link";
import { ArrowRight, Bot, FileSearch, ShieldCheck } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-50">
      <section className="bg-gradient-to-br from-slate-950 via-blue-950 to-blue-700 px-6 py-16 text-white md:py-24">
        <div className="mx-auto max-w-6xl">
          <div className="flex items-center gap-3 text-sm font-semibold text-blue-200">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/10"><Bot size={21} /></div>
            NagrikSetu
          </div>
          <div className="mt-20 max-w-3xl">
            <p className="mb-4 font-semibold uppercase tracking-[0.18em] text-cyan-300">Citizen services, made clearer</p>
            <h1 className="text-5xl font-bold leading-tight md:text-7xl">Understand your government benefits.</h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-blue-100">Ask the civic assistant, explore verified schemes, and keep your application tracking in one place.</p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Link href="/chat" className="inline-flex items-center gap-2 rounded-xl bg-cyan-300 px-5 py-3 font-bold text-slate-950 hover:bg-cyan-200">Ask Citizen AI <ArrowRight size={18} /></Link>
              <Link href="/services" className="rounded-xl border border-white/30 px-5 py-3 font-bold text-white hover:bg-white/10">Explore schemes</Link>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-5 px-6 py-12 md:grid-cols-3">
        <Link href="/chat" className="rounded-2xl border bg-white p-6 shadow-sm hover:border-blue-400">
          <Bot className="text-blue-600" size={28} />
          <h2 className="mt-5 text-xl font-bold text-slate-900">Ask in plain language</h2>
          <p className="mt-2 leading-7 text-slate-600">Get guidance on eligibility, documents, benefits, and how to apply.</p>
        </Link>
        <Link href="/services" className="rounded-2xl border bg-white p-6 shadow-sm hover:border-blue-400">
          <FileSearch className="text-blue-600" size={28} />
          <h2 className="mt-5 text-xl font-bold text-slate-900">Browse live schemes</h2>
          <p className="mt-2 leading-7 text-slate-600">Search the scheme catalogue served by the NagrikSetu backend.</p>
        </Link>
        <Link href="/applications" className="rounded-2xl border bg-white p-6 shadow-sm hover:border-blue-400">
          <ShieldCheck className="text-blue-600" size={28} />
          <h2 className="mt-5 text-xl font-bold text-slate-900">Track your progress</h2>
          <p className="mt-2 leading-7 text-slate-600">Find submitted applications by phone number or tracking ID.</p>
        </Link>
      </section>
    </main>
  );
}
