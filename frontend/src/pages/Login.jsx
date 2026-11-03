import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { getErrorMessage, login } from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
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
      const data = await login(form);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/dashboard");
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
        <p className="eyebrow">WELCOME BACK</p>
        <h1>Log in to LinkShelf</h1>
        <p className="muted">Your saved websites are right where you left them.</p>
        {location.state?.message && <div className="success-alert">{location.state.message}</div>}
        <form className="auth-form" onSubmit={submit}>
          <label>Email address<input name="email" type="email" value={form.email} onChange={update} required placeholder="you@example.com" /></label>
          <label>Password<input name="password" type="password" value={form.password} onChange={update} required placeholder="Your password" /></label>
          {error && <div className="alert">{error}</div>}
          <button className="button button-primary button-full" disabled={loading}>{loading ? "Logging in…" : "Log in"}</button>
        </form>
        <p className="auth-switch">New to LinkShelf? <Link to="/signup">Create an account</Link></p>
      </section>
      <aside className="auth-aside">
        <div className="aside-orb orb-one"></div><div className="aside-orb orb-two"></div>
        <div className="aside-copy"><span className="aside-kicker">Your personal web library</span><h2>Less searching.<br />More discovering.</h2><p>One simple home for all the pages worth keeping.</p></div>
        <div className="floating-preview"><div className="floating-image"></div><div className="floating-lines"><i></i><i></i><i></i></div></div>
      </aside>
    </main>
  );
}
