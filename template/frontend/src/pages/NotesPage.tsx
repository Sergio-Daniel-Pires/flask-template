import { useEffect, useState, type FormEvent } from "react";

import { api, type Note } from "../lib/api";

export default function NotesPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    api.notes
      .list()
      .then((response) => {
        if (active) setNotes(response.result);
      })
      .catch((requestError: unknown) => {
        if (active) {
          setError(
            requestError instanceof Error ? requestError.message : "Unknown error",
          );
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = text.trim();
    if (!value) return;

    setPending(true);
    setError(null);

    try {
      const response = await api.notes.create(value);
      setNotes((current) => [response.result, ...current]);
      setText("");
    } catch (requestError: unknown) {
      setError(
        requestError instanceof Error ? requestError.message : "Unknown error",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="stack narrow">
      <header>
        <p className="eyebrow">SQLite + SQLAlchemy</p>
        <h1>Notes</h1>
        <p className="lede">
          Minimal persistence example: the form writes to SQLite and the list
          reloads from the backend.
        </p>
      </header>

      <form className="card form" onSubmit={handleSubmit}>
        <label htmlFor="note-text">New note</label>
        <input
          id="note-text"
          name="note-text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          maxLength={500}
          required
          autoComplete="off"
          placeholder="Write something…"
        />
        <button type="submit" disabled={pending}>
          {pending ? "Saving…" : "Add"}
        </button>
      </form>

      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}

      <article className="card">
        <h2>Saved</h2>
        {loading ? (
          <p className="muted">Loading…</p>
        ) : notes.length === 0 ? (
          <p className="muted">No notes yet.</p>
        ) : (
          <ul className="notes" data-testid="notes-list">
            {notes.map((note) => (
              <li key={note.id}>
                <span>{note.text}</span>
                <time dateTime={note.created_at}>
                  {new Date(note.created_at).toLocaleString("en-US")}
                </time>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  );
}
