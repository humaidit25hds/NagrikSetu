import { Bot, User } from "lucide-react";

type MessageProps = {
  sender: "ai" | "user";
  text: string;
};

export default function Message({
  sender,
  text,
}: MessageProps) {
  const isUser = sender === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-[80%] items-start gap-3 ${
          isUser ? "flex-row-reverse" : ""
        }`}
      >
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
            isUser
              ? "bg-slate-900 text-white"
              : "bg-blue-100 text-blue-600"
          }`}
        >
          {isUser ? <User size={19} /> : <Bot size={19} />}
        </div>

        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-6 ${
            isUser
              ? "rounded-tr-sm bg-blue-600 text-white"
              : "rounded-tl-sm bg-slate-100 text-slate-800"
          }`}
        >
          {text}
        </div>
      </div>
    </div>
  );
}