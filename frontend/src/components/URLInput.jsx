import { useState } from "react";

export default function URLInput({ onSubmit, loading }) {
  const [url, setUrl] = useState("");

  function submit(event) {
    event.preventDefault();
    if (url.trim()) onSubmit(url.trim());
  }

  return (
    <form className="url-form" onSubmit={submit}>
      <label htmlFor="website-url">Website URL</label>
      <div className="url-control">
        <span className="url-icon">↗</span>
        <input
          id="website-url"
          type="url"
          required
          placeholder="https://example.com"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
        />
        <button className="button button-primary" disabled={loading}>
          {loading ? "Generating…" : "Add preview"}
        </button>
      </div>
      <p className="helper-text">Paste a public website link. We’ll fetch its title, description and preview image.</p>
    </form>
  );
}
