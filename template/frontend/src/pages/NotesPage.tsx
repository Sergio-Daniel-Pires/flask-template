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
            requestError instanceof Error ? requestError.message : "Erro desconhecido",
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
        requestError instanceof Error ? requestError.message : "Erro desconhecido",
      );
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="stack narrow">
      <header>
        <p className="eyebrow">SQLite + SQLAlchemy</p>
        <h1>Notas</h1>
        <p className="lede">
          Exemplo mínimo de persistência: o formulário grava no SQLite e a lista
          recarrega do backend.
        </p>
      </header>

      <form className="card form" onSubmit={handleSubmit}>
        <label htmlFor="note-text">Nova nota</label>
        <input
          id="note-text"
          name="note-text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          maxLength={500}
          required
          autoComplete="off"
          placeholder="Escreva algo…"
        />
        <button type="submit" disabled={pending}>
          {pending ? "Salvando…" : "Adicionar"}
        </button>
      </form>

      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}

      <article className="card">
        <h2>Salvas</h2>
        {loading ? (
          <p className="muted">Carregando…</p>
        ) : notes.length === 0 ? (
          <p className="muted">Nenhuma nota ainda.</p>
        ) : (
          <ul className="notes" data-testid="notes-list">
            {notes.map((note) => (
              <li key={note.id}>
                <span>{note.text}</span>
                <time dateTime={note.created_at}>
                  {new Date(note.created_at).toLocaleString("pt-BR")}
                </time>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  );
}
