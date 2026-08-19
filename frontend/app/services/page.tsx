import Link from "next/link";
import {
  ArrowLeft,
  Search,
  GraduationCap,
  HeartPulse,
  Home,
  Briefcase,
  Landmark,
  Users,
} from "lucide-react";

const services = [
  {
    title: "Education & Scholarships",
    description:
      "Find scholarships, education schemes, student benefits and financial assistance.",
    icon: GraduationCap,
    category: "Education",
  },
  {
    title: "Health Services",
    description:
      "Explore health insurance, medical assistance and government healthcare schemes.",
    icon: HeartPulse,
    category: "Health",
  },
  {
    title: "Housing & Shelter",
    description:
      "Discover housing schemes and assistance programs for eligible citizens.",
    icon: Home,
    category: "Housing",
  },
  {
    title: "Employment & Jobs",
    description:
      "Find employment schemes, skill development programs and job-related services.",
    icon: Briefcase,
    category: "Employment",
  },
  {
    title: "Financial Assistance",
    description:
      "Explore pensions, financial support and welfare programs provided by the government.",
    icon: Landmark,
    category: "Finance",
  },
  {
    title: "Social Welfare",
    description:
      "Find government programs designed to support families, senior citizens and communities.",
    icon: Users,
    category: "Welfare",
  },
];

export default function ServicesPage() {
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
      <section className="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-16 text-white">
        <div className="mx-auto max-w-6xl">
          <p className="mb-3 font-medium text-blue-100">
            Government Services
          </p>

          <h1 className="text-4xl font-bold md:text-5xl">
            Find Services Made for You
          </h1>

          <p className="mt-5 max-w-2xl text-lg leading-8 text-blue-100">
            Explore government services, schemes and welfare programs
            in one simple place.
          </p>
        </div>
      </section>

      {/* Search */}
      <section className="mx-auto max-w-6xl px-6 py-8">
        <div className="flex items-center gap-3 rounded-2xl border bg-white px-4 py-3 shadow-sm">
          <Search size={22} className="text-slate-400" />

          <input
            type="text"
            placeholder="Search government services..."
            className="w-full bg-transparent text-slate-900 outline-none placeholder:text-slate-400"
          />
        </div>
      </section>

      {/* Services */}
      <section className="mx-auto max-w-6xl px-6 pb-16">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900">
            Popular Services
          </h2>

          <p className="mt-2 text-slate-600">
            Browse services by category.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {services.map((service) => {
            const Icon = service.icon;

            return (
              <div
                key={service.title}
                className="group rounded-2xl border bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-blue-600">
                  <Icon size={25} />
                </div>

                <p className="mb-2 text-sm font-medium text-blue-600">
                  {service.category}
                </p>

                <h3 className="text-xl font-bold text-slate-900">
                  {service.title}
                </h3>

                <p className="mt-3 leading-7 text-slate-600">
                  {service.description}
                </p>

                <Link
                  href="/chat"
                  className="mt-6 inline-flex items-center font-semibold text-blue-600 hover:text-blue-700"
                >
                  Ask Citizen AI →
                </Link>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}