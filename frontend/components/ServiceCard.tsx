import Link from "next/link";
import { ArrowRight, LucideIcon } from "lucide-react";

type ServiceCardProps = {
  title: string;
  description: string;
  icon: LucideIcon;
  category?: string;
};

export default function ServiceCard({
  title,
  description,
  icon: Icon,
  category,
}: ServiceCardProps) {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
      <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-blue-600">
        <Icon size={25} />
      </div>

      {category && (
        <p className="mb-2 text-sm font-medium text-blue-600">
          {category}
        </p>
      )}

      <h3 className="text-xl font-bold text-slate-900">
        {title}
      </h3>

      <p className="mt-3 leading-7 text-slate-600">
        {description}
      </p>

      <Link
        href="/chat"
        className="mt-6 inline-flex items-center gap-2 font-semibold text-blue-600 hover:text-blue-700"
      >
        Ask Citizen AI
        <ArrowRight size={17} />
      </Link>
    </div>
  );
}