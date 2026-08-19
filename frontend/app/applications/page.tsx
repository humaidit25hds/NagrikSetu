"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  CheckCircle2,
  Clock,
  FileText,
  Search,
} from "lucide-react";
import { getApplications, submitApplication, trackApplication, type Application } from "../../lib/api";

function statusStyles(status: string) {
  const normalized = status.toUpperCase();
  if (["APPROVED", "COMPLETED", "SUBMITTED"].includes(normalized)) {
    return { className: "bg-green-50 text-green-700", icon: <CheckCircle2 size={17} /> };
  }
  return { className: "bg-amber-50 text-amber-700", icon: <Clock size={17} /> };
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-IN", { dateStyle: "medium" }).format(new Date(value));
}

export default function ApplicationsPage() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [trackingNumber, setTrackingNumber] = useState("");
  const [serviceId, setServiceId] = useState("");
  const [applicantName, setApplicantName] = useState("");
  const [applications, setApplications] = useState<Application[]>([]);
  const [trackedApplication, setTrackedApplication] = useState<Application | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadApplications = async (event: FormEvent) => {
    event.preventDefault();
    if (!phoneNumber.trim()) return;
    setIsLoading(true);
    setError(null);
    setTrackedApplication(null);
    try {
      setApplications(await getApplications(phoneNumber.trim()));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load applications.");
    } finally {
      setIsLoading(false);
    }
  };

  const track = async (event: FormEvent) => {
    event.preventDefault();
    if (!trackingNumber.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      setTrackedApplication(await trackApplication(trackingNumber.trim()));
    } catch (requestError) {
      setTrackedApplication(null);
      setError(requestError instanceof Error ? requestError.message : "Application not found.");
    } finally {
      setIsLoading(false);
    }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!serviceId || !applicantName.trim() || !phoneNumber.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const created = await submitApplication({
        service_id: Number(serviceId),
        applicant_name: applicantName.trim(),
        applicant_phone: phoneNumber.trim(),
      });
      setTrackedApplication(created);
      setApplications(await getApplications(phoneNumber.trim()));
      setServiceId("");
      setApplicantName("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to submit application.");
    } finally {
      setIsLoading(false);
    }
  };

  const visibleApplications = trackedApplication ? [trackedApplication] : applications;

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

      <section className="bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-14 text-white">
        <div className="mx-auto max-w-6xl">
          <p className="mb-3 text-indigo-100">Citizen Dashboard</p>
          <h1 className="text-4xl font-bold">My Applications</h1>
          <p className="mt-4 max-w-2xl text-indigo-100">Look up applications using the phone number used during submission or a tracking number.</p>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-10">
        <div className="grid gap-4 md:grid-cols-2">
          <form onSubmit={loadApplications} className="rounded-2xl border bg-white p-5 shadow-sm">
            <label htmlFor="phone" className="text-sm font-semibold text-slate-900">Find by phone number</label>
            <div className="mt-3 flex gap-2">
              <input id="phone" value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} placeholder="9876543210" className="min-w-0 flex-1 rounded-xl border px-3 py-2 text-slate-900 outline-none focus:border-blue-500" />
              <button type="submit" disabled={isLoading} className="rounded-xl bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700 disabled:opacity-50">Search</button>
            </div>
          </form>
          <form onSubmit={track} className="rounded-2xl border bg-white p-5 shadow-sm">
            <label htmlFor="tracking" className="text-sm font-semibold text-slate-900">Track an application</label>
            <div className="mt-3 flex gap-2">
              <input id="tracking" value={trackingNumber} onChange={(event) => setTrackingNumber(event.target.value)} placeholder="NS-2026-ABC123" className="min-w-0 flex-1 rounded-xl border px-3 py-2 text-slate-900 outline-none focus:border-blue-500" />
              <button type="submit" disabled={isLoading} className="flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-700 disabled:opacity-50"><Search size={16} />Track</button>
            </div>
          </form>
        </div>

        <form onSubmit={submit} className="mt-4 rounded-2xl border bg-white p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-900">Submit a new application</h2>
          <div className="mt-3 grid gap-3 md:grid-cols-3">
            <input value={serviceId} onChange={(event) => setServiceId(event.target.value)} type="number" min="1" placeholder="Scheme ID" aria-label="Scheme ID" className="rounded-xl border px-3 py-2 text-slate-900 outline-none focus:border-blue-500" />
            <input value={applicantName} onChange={(event) => setApplicantName(event.target.value)} placeholder="Applicant name" aria-label="Applicant name" className="rounded-xl border px-3 py-2 text-slate-900 outline-none focus:border-blue-500" />
            <button type="submit" disabled={isLoading} className="rounded-xl bg-cyan-600 px-4 py-2 font-semibold text-white hover:bg-cyan-700 disabled:opacity-50">Submit application</button>
          </div>
          <p className="mt-2 text-xs text-slate-500">Use a scheme ID from the Services page and the phone number above.</p>
        </form>

        {error && <p className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error}</p>}
        {!isLoading && !error && visibleApplications.length === 0 && (
          <div className="mt-8 flex gap-3 rounded-2xl border border-blue-100 bg-blue-50 p-5 text-blue-800">
            <AlertCircle className="mt-0.5 shrink-0" size={20} />
            <p className="text-sm leading-6">Enter the phone number used for an application or its tracking number to see live status.</p>
          </div>
        )}

        {isLoading && <p className="mt-8 text-slate-600">Loading application status...</p>}
        <div className="mt-8 space-y-5">
          {visibleApplications.map((application) => {
            const status = statusStyles(application.status);
            return (
              <article key={application.id} className="rounded-2xl border bg-white p-6 shadow-sm">
                <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                  <div className="flex items-start gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-blue-600"><FileText size={24} /></div>
                    <div>
                      <h2 className="text-lg font-bold text-slate-900">{application.service_title ?? "Government Scheme"}</h2>
                      <p className="mt-1 text-slate-600">Tracking: {application.tracking_number}</p>
                      <p className="mt-2 text-sm text-slate-400">Submitted {formatDate(application.submitted_at)}</p>
                      {application.remarks && <p className="mt-3 text-sm leading-6 text-slate-600">{application.remarks}</p>}
                    </div>
                  </div>
                  <div className={`flex items-center gap-2 self-start rounded-full px-4 py-2 text-sm font-semibold md:self-auto ${status.className}`}>
                    {status.icon}
                    {application.status}
                  </div>
                </div>
              </article>
            );
          })}
        </div>

        <div className="mt-8 flex justify-end">
          <Link href="/services" className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700">Find a Service</Link>
        </div>
      </section>
    </main>
  );
}
