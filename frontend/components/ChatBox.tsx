"use client";

import { useState } from "react";
import { Send } from "lucide-react";
import Message from "./Message";

type ChatMessage = {
  id: number;
  sender: "ai" | "user";
  text: string;
};

export default function ChatBox() {
  const [input, setInput] = useState("");

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      sender: "ai",
      text: "Hello! I'm Citizen AI. How can I help you with government services today?",
    },
  ]);

  const sendMessage = () => {
    const text = input.trim();

    if (!text) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        id: Date.now(),
        sender: "user",
        text,
      },
    ]);

    setInput("");

    setTimeout(() => {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          sender: "ai",
          text: "I'm currently in demo mode. The backend AI will be connected later to provide real government service information.",
        },
      ]);
    }, 700);
  };

  return (
    <div className="flex flex-1 flex-col overflow-hidden rounded-3xl border bg-white shadow-xl">
      <div className="flex-1 space-y-5 overflow-y-auto p-6">
        {messages.map((message) => (
          <Message
            key={message.id}
            sender={message.sender}
            text={message.text}
          />
        ))}
      </div>

      <div className="border-t bg-white p-4">
        <div className="flex items-center gap-3 rounded-2xl border bg-slate-50 p-2 focus-within:border-blue-500">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask about a government scheme or service..."
            className="flex-1 bg-transparent px-3 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400"
          />

          <button
            onClick={sendMessage}
            className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white hover:bg-blue-700"
          >
            <Send size={19} />
          </button>
        </div>
      </div>
    </div>
  );
}