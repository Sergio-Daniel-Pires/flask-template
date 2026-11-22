import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <section className="stack narrow">
      <p className="eyebrow">404</p>
      <h1>Page not found</h1>
      <p className="lede">The address you visited does not exist in this project.</p>
      <Link className="button" to="/">
        Back to home
      </Link>
    </section>
  );
}
