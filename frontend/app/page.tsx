import Link from "next/link";
import {
  Bot,
  FileText,
  Search,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";

export default function Home() {
  return (
    <main>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-700 to-indigo-800 text-white">
        <div className="mx-auto max-w-7xl px-6 py-24">
          <div className="max-w-3xl">

            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2">
              <ShieldCheck size={18} />
              Trusted Citizen Services
            </div>

            {/* Heading */}
            <h1 className="text-4xl font-bold leading-tight md:text-6xl">
              Your Smart Guide to Government Services
            </h1>

            {/* Description */}
            <p className="mt-6 text-lg text-blue-100 md:text-xl">
              Citizen AI helps you discover government services,
              understand eligibility requirements, and get guidance
              for applications using simple language.
            </p>

            {/* Buttons */}
            <div className="mt-8 flex flex-wrap gap-4">

              <Link
                href="/chat"
                className="flex items-center gap-2 rounded-lg bg-white px-6 py-3 font-semibold text-blue-700 hover:bg-blue-50"
              >
                <Bot size={20} />
                Ask Citizen AI
              </Link>

              <Link
                href="/services"
                className="flex items-center gap-2 rounded-lg border border-white px-6 py-3 font-semibold hover:bg-white/10"
              >
                Explore Services
                <ArrowRight size={18} />
              </Link>

            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="mx-auto max-w-7xl px-6 py-20">

        {/* Section Heading */}
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold">
            What Citizen AI Can Do
          </h2>

          <p className="mt-3 text-slate-600">
            One platform for easier access to government information.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid gap-6 md:grid-cols-3">

          <FeatureCard
            icon={<Bot />}
            title="AI Assistant"
            description="Ask questions about government schemes and services in simple language."
            href="/chat"
          />

          <FeatureCard
            icon={<Search />}
            title="Find Services"
            description="Search and discover government services that may be useful to you."
            href="/services"
          />

          <FeatureCard
            icon={<FileText />}
            title="Applications"
            description="Track and manage your service applications from one place."
            href="/applications"
          />

        </div>
      </section>

      {/* Call To Action Section */}
      <section className="bg-slate-100 px-6 py-20 text-center">

        <h2 className="text-3xl font-bold">
          Need help finding a government service?
        </h2>

        <p className="mx-auto mt-4 max-w-2xl text-slate-600">
          Ask Citizen AI and get step-by-step guidance.
        </p>

        <Link
          href="/chat"
          className="mt-7 inline-flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
        >
          Start Chat
          <ArrowRight size={18} />
        </Link>

      </section>
    </main>
  );
}


/* Feature Card Component */
function FeatureCard({
  icon,
  title,
  description,
  href,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="rounded-xl border bg-white p-7 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
    >

      {/* Icon */}
      <div className="mb-5 w-fit rounded-lg bg-blue-100 p-3 text-blue-600">
        {icon}
      </div>

      {/* Title */}
      <h3 className="text-xl font-bold">
        {title}
      </h3>

      {/* Description */}
      <p className="mt-3 text-slate-600">
        {description}
      </p>

      {/* Link */}
      <div className="mt-5 flex items-center gap-2 font-semibold text-blue-600">
        Learn more
        <ArrowRight size={17} />
      </div>

    </Link>
  );
}