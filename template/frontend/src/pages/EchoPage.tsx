import { useState, type FormEvent } from "react";

import { api } from "../lib/api";

const ECHO_TYPES = [
  { value: "None", label: "Normal" },
  { value: "Reverse", label: "Invertido" },
  { value: "Mirror", label: "Espelhado" },
];

export default function EchoPage() {
  const [message, setMessage] = useState("Hello World");
  const [echoType, setEchoType] = useState("None");
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.echo(message, echoType);
      setResult(response.result);
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
        <p className="eyebrow">POST /api/echo/string</p>
        <h1>Echo</h1>
        <p className="lede">
          Envie uma mensagem e escolha como o backend deve transformá-la.
        </p>
      </header>

      <form className="card form" onSubmit={handleSubmit}>
        <label htmlFor="message">Mensagem</label>
        <input
          id="message"
          name="message"
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          required
          maxLength={500}
          autoComplete="off"
        />

        <label htmlFor="echo-type">Tipo de echo</label>
        <select
          id="echo-type"
          name="echo-type"
          value={echoType}
          onChange={(event) => setEchoType(event.target.value)}
        >
          {ECHO_TYPES.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>

        <button type="submit" disabled={pending}>
          {pending ? "Enviando…" : "Enviar"}
        </button>
      </form>

      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}

      {result !== null ? (
        <article className="card result">
          <h2>Resposta</h2>
          <pre data-testid="echo-result">{result}</pre>
        </article>
      ) : null}
    </section>
  );
}
