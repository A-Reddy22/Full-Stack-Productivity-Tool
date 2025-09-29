import React, { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import { TaskForm } from "./components/TaskForm";
import { TaskList } from "./components/TaskList";

export type Priority = { id: number; name: string; rank: number };
export type Task = {
  id: number;
  title: string;
  description?: string | null;
  due_date?: string | null;
  completed: boolean;
  priority?: Priority | null;
  created_at: string;
  updated_at: string;
};

export default function App() {
  const [priorities, setPriorities] = useState<Priority[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  const reload = async () => {
    setLoading(true);
    try {
      const pri = await api<Priority[]>("/priorities");
      setPriorities(pri);
      const data = await api<{ items: Task[] }>("/tasks?page=1&page_size=50");
      setTasks(data.items);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { reload(); }, []);

  const onCreate = async (payload: Partial<Task> & { title: string }) => {
    await api<Task>("/tasks", { method: "POST", body: JSON.stringify(payload) });
    await reload();
  };

  const onToggle = async (task: Task) => {
    await api<Task>(`/tasks/${task.id}`, { method: "PATCH", body: JSON.stringify({ completed: !task.completed }) });
    await reload();
  };

  const onDelete = async (id: number) => {
    await fetch(`${(import.meta as any).env.VITE_API_BASE || "http://localhost:5000"}/api/tasks/${id}`, { method: "DELETE" });
    await reload();
  };

  const sorted = useMemo(() => tasks, [tasks]);

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 16, fontFamily: "sans-serif" }}>
      <h1>Productivity Tool</h1>
      <TaskForm priorities={priorities} onCreate={onCreate} />
      {loading ? <p>Loading…</p> : <TaskList tasks={sorted} onToggle={onToggle} onDelete={onDelete} />}
    </div>
  );
}
