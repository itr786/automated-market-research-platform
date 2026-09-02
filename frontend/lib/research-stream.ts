export type ResearchEvent = {
  status: "queued" | "running" | "complete" | "failed" | "cancelled";
  progress: number;
  message: string;
};

export function subscribeToResearch(
  briefId: number,
  onEvent: (event: ResearchEvent) => void,
  onStateChange?: (connected: boolean) => void,
) {
  const base = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000";
  const socket = new WebSocket(`${base}/ws/research/${briefId}/`);
  socket.onopen = () => onStateChange?.(true);
  socket.onclose = () => onStateChange?.(false);
  socket.onmessage = ({ data }) => onEvent(JSON.parse(data) as ResearchEvent);
  return () => socket.close();
}
