import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getErrorMessage, signup } from "../services/api";

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      await signup(form);
      navigate("/login", { state: { message: "Account created. Please log in." } });
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-brand"><span className="brand-mark">L</span> LinkShelf</div>
        <p className="eyebrow">YOUR LINKS, BEAUTIFULLY ORGANIZED</p>
        <h1>Create your account</h1>
        <p className="muted">Save website previews and find them whenever you need.</p>
        <form className="auth-form" onSubmit={submit}>
          <label>Full name<input name="full_name" value={form.full_name} onChange={update} required minLength="2" maxLength="100" placeholder="Your name" /></label>
          <label>Email address<input name="email" type="email" value={form.email} onChange={update} required placeholder="you@example.com" /></label>
          <label>Password<input name="password" type="password" value={form.password} onChange={update} required minLength="8" placeholder="At least 8 characters" /></label>
          {error && <div className="alert">{error}</div>}
          <button className="button button-primary button-full" disabled={loading}>{loading ? "Creating account…" : "Create account"}</button>
        </form>
        <p className="auth-switch">Already have an account? <Link to="/login">Log in</Link></p>
      </section>
      <aside className="auth-aside">
        <div className="aside-orb orb-one"></div><div className="aside-orb orb-two"></div>
        <div className="aside-copy"><span className="aside-kicker">A calmer corner of the web</span><h2>Keep the good<br />things you find.</h2><p>Turn any link into a visual bookmark you can come back to.</p></div>
        <div className="floating-preview"><div className="floating-image"></div><div className="floating-lines"><i></i><i></i><i></i></div></div>
      </aside>
    </main>
  );
}
