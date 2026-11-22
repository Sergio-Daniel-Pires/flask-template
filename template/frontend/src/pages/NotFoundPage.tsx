import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <section className="stack narrow">
      <p className="eyebrow">404</p>
      <h1>Página não encontrada</h1>
      <p className="lede">O endereço acessado não existe neste projeto.</p>
      <Link className="button" to="/">
        Voltar para o início
      </Link>
    </section>
  );
}
