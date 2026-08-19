import Link from "next/link";
import {
  ArrowLeft,
  FileText,
  Clock,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

const applications = [
  {
    id: 1,
    title: "Student Scholarship Application",
    service: "Education Scholarship",
    status: "In Progress",
    date: "19 Aug 2026",
    statusType: "progress",
  },
  {
    id: 2,
    title: "Health Assistance Application",
    service: "Government Health Scheme",
    status: "Submitted",
    date: "15 Aug 2026",
    statusType: "submitted",
  },
];

export default function ApplicationsPage() {
  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link
            href="/"
            className="flex items-center gap-2 font-semibold text-slate-900"
          >
            <ArrowLeft size={20} />
            Back to Home
          </Link>

          <div className="font-bold text-blue-600">
            Citizen AI
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-14 text-white">
        <div className="mx-auto max-w-6xl">
          <p className="mb-3 text-indigo-100">
            Citizen Dashboard
          </p>

          <h1 className="text-4xl font-bold">
            My Applications
          </h1>

          <p className="mt-4 max-w-2xl text-indigo-100">
            Track and manage your government service applications
            from one place.
          </p>
        </div>
      </section>

      {/* Applications */}
      <section className="mx-auto max-w-6xl px-6 py-10">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">
              Your Applications
            </h2>

            <p className="mt-2 text-slate-600">
              View the current status of your applications.
            </p>
          </div>

          <Link
            href="/services"
            className="rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            Find a Service
          </Link>
        </div>

        <div className="space-y-5">
          {applications.map((application) => (
            <div
              key={application.id}
              className="rounded-2xl border bg-white p-6 shadow-sm"
            >
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-blue-600">
                    <FileText size={24} />
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-slate-900">
                      {application.title}
                    </h3>

                    <p className="mt-1 text-slate-600">
                      {application.service}
                    </p>

                    <p className="mt-2 text-sm text-slate-400">
                      Applied on {application.date}
                    </p>
                  </div>
                </div>

                <div>
                  {application.statusType === "progress" ? (
                    <div className="flex items-center gap-2 rounded-full bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700">
                      <Clock size={17} />
                      {application.status}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 rounded-full bg-green-50 px-4 py-2 text-sm font-semibold text-green-700">
                      <CheckCircle2 size={17} />
                      {application.status}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {/* Information */}
          <div className="flex gap-3 rounded-2xl border border-blue-100 bg-blue-50 p-5 text-blue-800">
            <AlertCircle className="mt-0.5 shrink-0" size={20} />

            <p className="text-sm leading-6">
              Application information shown here is currently demo data.
              Real application tracking will be connected to the backend
              later.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}