import Link from "next/link";
import { Bot } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="border-b bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link
          href="/"
          className="flex items-center gap-2"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white">
            <Bot size={20} />
          </div>

          <span className="text-lg font-bold text-slate-900">
            Citizen AI
          </span>
        </Link>

        <div className="hidden items-center gap-6 md:flex">
          <Link
            href="/"
            className="text-sm font-medium text-slate-600 hover:text-blue-600"
          >
            Home
          </Link>

          <Link
            href="/chat"
            className="text-sm font-medium text-slate-600 hover:text-blue-600"
          >
            AI Assistant
          </Link>

          <Link
            href="/services"
            className="text-sm font-medium text-slate-600 hover:text-blue-600"
          >
            Services
          </Link>

          <Link
            href="/applications"
            className="text-sm font-medium text-slate-600 hover:text-blue-600"
          >
            Applications
          </Link>
        </div>
      </div>
    </nav>
  );
}