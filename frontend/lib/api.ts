const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendChatMessage(message: string) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to connect to the Citizen AI backend.");
  }

  return response.json();
}

export async function getServices() {
  const response = await fetch(`${API_URL}/services`);

  if (!response.ok) {
    throw new Error("Unable to load government services.");
  }

  return response.json();
}

export async function getApplications() {
  const response = await fetch(`${API_URL}/applications`);

  if (!response.ok) {
    throw new Error("Unable to load applications.");
  }

  return response.json();
}