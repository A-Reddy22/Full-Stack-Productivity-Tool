import React, { useState } from "react";
import type { Priority } from "../App";

export function TaskForm({ priorities, onCreate }: {
  priorities: Priority[];
  onCreate: (p: { title: string; description?: string; due_date?: string | null; priority_id?: number | null }) => Promise<void>;
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [due, setDue] = useState<string>("");
  const [priorityId, setPriorityId] = useState<number | "">("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    await onCreate({
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: due || null,
      priority_id: priorityId === "" ? null : Number(priorityId)
    });
    setTitle("");
    setDescription("");
    setDue("");
    setPriorityId("");
  };

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr 1fr 1fr auto", alignItems: "end", marginBottom: 16 }}>
      <div>
        <label>Title<br/>
          <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Task title" required style={{ width: "100%" }} />
        </label>
      </div>
      <div>
        <label>Description<br/>
          <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Optional" style={{ width: "100%" }} />
        </label>
      </div>
      <div>
        <label>Due date<br/>
          <input type="date" value={due} onChange={e => setDue(e.target.value)} style={{ width: "100%" }} />
        </label>
      </div>
      <div>
        <label>Priority<br/>
          <select value={priorityId} onChange={e => setPriorityId(e.target.value === "" ? "" : Number(e.target.value))} style={{ width: "100%" }}>
            <option value="">None</option>
            {priorities.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </label>
      </div>
      <button type="submit" style={{ gridColumn: "1 / -1" }}>Add Task</button>
    </form>
  );
}
