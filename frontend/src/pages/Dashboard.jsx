import { useCallback, useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import URLInput from "../components/URLInput";
import PreviewCard from "../components/PreviewCard";
import { createPreview, deleteSavedUrl, getErrorMessage, getMe, getSavedUrls } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("user") || "null"); } catch { return null; }
  });
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const loadData = useCallback(async () => {
    try {
      const [profile, saved] = await Promise.all([getMe(), getSavedUrls()]);
      setUser(profile);
      localStorage.setItem("user", JSON.stringify(profile));
      setItems(saved);
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login");
      } else {
        setError(getErrorMessage(err));
      }
    } finally {
      setPageLoading(false);
    }
  }, [navigate]);

  useEffect(() => { loadData(); }, [loadData]);

  async function addUrl(url) {
    setError("");
    setNotice("");
    setLoading(true);
    try {
      const saved = await createPreview(url);
      setItems((current) => [saved, ...current]);
      setNotice("Website preview saved successfully.");
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  async function removeUrl(id) {
    try {
      await deleteSavedUrl(id);
      setItems((current) => current.filter((item) => item.id !== id));
      setNotice("Saved website deleted.");
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }

  return (
    <div className="app-shell">
      <Navbar user={user} />
      <main className="dashboard">
        <section className="hero">
          <div>
            <p className="eyebrow">YOUR PERSONAL WEB LIBRARY</p>
            <h1>Good links deserve<br /><span>a place to live.</span></h1>
            <p className="hero-subtitle">Save a website and we’ll turn it into a visual preview.</p>
          </div>
          <div className="hero-decoration"><div className="decoration-card card-back"></div><div className="decoration-card card-front"><span>↗</span><i></i><i></i></div></div>
        </section>

        <section className="add-section">
          <URLInput onSubmit={addUrl} loading={loading} />
        </section>

        {error && <div className="alert dashboard-alert">{error}</div>}
        {notice && <div className="success-alert dashboard-alert">{notice}</div>}

        <section className="saved-section">
          <div className="section-heading">
            <div><p className="eyebrow">COLLECTION</p><h2>Your saved websites <span className="count">{items.length}</span></h2></div>
          </div>
          {pageLoading ? <div className="empty-state">Loading your collection…</div> :
            items.length ? <div className="preview-grid">{items.map((item) => <PreviewCard key={item.id} item={item} onDelete={removeUrl} />)}</div> :
            <div className="empty-state"><div className="empty-icon">↗</div><h3>Your collection starts here</h3><p>Paste a website URL above to create your first preview.</p></div>}
        </section>
        <footer className="footer">LinkShelf <span>·</span> Keep what inspires you.</footer>
      </main>
    </div>
  );
}
