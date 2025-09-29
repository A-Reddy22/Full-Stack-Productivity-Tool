import React from "react";
import type { Task } from "../App";

export function TaskList({ tasks, onToggle, onDelete }: {
  tasks: Task[];
  onToggle: (t: Task) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}) {
  if (!tasks.length) return <p>No tasks yet.</p>;
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: 8 }}>
      {tasks.map(t => (
        <li key={t.id} style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, display: "grid", gap: 4 }}>
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <input type="checkbox" checked={t.completed} onChange={() => onToggle(t)} />
            <strong style={{ textDecoration: t.completed ? "line-through" : "none" }}>{t.title}</strong>
            {t.priority ? <span style={{ marginLeft: "auto" }}>{t.priority.name}</span> : null}
          </div>
          {t.description ? <div>{t.description}</div> : null}
          <div style={{ fontSize: 12, color: "#666" }}>
            {t.due_date ? `Due: ${t.due_date}` : "No due date"}
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={() => onDelete(t.id)} style={{ color: "#b00" }}>Delete</button>
          </div>
        </li>
      ))}
    </ul>
  );
}
