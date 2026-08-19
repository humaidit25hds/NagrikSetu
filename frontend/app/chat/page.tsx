"use client";

import { useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Bot,
  Send,
  User,
  ShieldCheck,
} from "lucide-react";

type Message = {
  id: number;
  sender: "ai" | "user";
  text: string;
};

export default function ChatPage() {
  const [input, setInput] = useState("");

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      sender: "ai",
      text: "Hello! I'm Citizen AI. I can help you understand government schemes, services, eligibility, and application procedures. How can I help you today?",
    },
  ]);

  const sendMessage = () => {
    const text = input.trim();

    if (!text) return;

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text,
    };

    setMessages((current) => [...current, userMessage]);
    setInput("");

    setTimeout(() => {
      const aiMessage: Message = {
        id: Date.now() + 1,
        sender: "ai",
        text: "Thanks for your question. I'm currently in demo mode. Once the backend AI service is connected, I will provide detailed information about government services and eligibility.",
      };

      setMessages((current) => [...current, aiMessage]);
    }, 700);
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link
            href="/"
            className="flex items-center gap-2 font-semibold text-slate-900"
          >
            <ArrowLeft size={20} />
            Back to Home
          </Link>

          <div className="flex items-center gap-2 text-sm text-slate-600">
            <ShieldCheck size={18} className="text-blue-600" />
            Trusted Citizen Services
          </div>
        </div>
      </header>

      {/* Chat Section */}
      <section className="mx-auto flex min-h-[calc(100vh-73px)] max-w-4xl flex-col px-4 py-8">
        {/* Title */}
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-lg">
            <Bot size={30} />
          </div>

          <h1 className="text-3xl font-bold text-slate-900">
            Ask Citizen AI
          </h1>

          <p className="mt-2 text-slate-600">
            Ask questions about government schemes and services.
          </p>
        </div>

        {/* Chat Box */}
        <div className="flex flex-1 flex-col overflow-hidden rounded-3xl border bg-white shadow-xl">
          {/* Chat Messages */}
          <div className="flex-1 space-y-5 overflow-y-auto p-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.sender === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`flex max-w-[80%] items-start gap-3 ${
                    message.sender === "user"
                      ? "flex-row-reverse"
                      : ""
                  }`}
                >
                  {/* Avatar */}
                  <div
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
                      message.sender === "user"
                        ? "bg-slate-900 text-white"
                        : "bg-blue-100 text-blue-600"
                    }`}
                  >
                    {message.sender === "user" ? (
                      <User size={19} />
                    ) : (
                      <Bot size={19} />
                    )}
                  </div>

                  {/* Message */}
                  <div
                    className={`rounded-2xl px-4 py-3 text-sm leading-6 ${
                      message.sender === "user"
                        ? "rounded-tr-sm bg-blue-600 text-white"
                        : "rounded-tl-sm bg-slate-100 text-slate-800"
                    }`}
                  >
                    {message.text}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="border-t bg-white p-4">
            <div className="flex items-center gap-3 rounded-2xl border bg-slate-50 p-2 focus-within:border-blue-500">
              <input
                type="text"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about a government scheme or service..."
                className="flex-1 bg-transparent px-3 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400"
              />

              <button
                onClick={sendMessage}
                className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-700"
                aria-label="Send message"
              >
                <Send size={19} />
              </button>
            </div>

            <p className="mt-2 text-center text-xs text-slate-400">
              Citizen AI provides guidance. Always verify important
              information with official government sources.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}