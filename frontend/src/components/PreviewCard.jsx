export default function PreviewCard({ item, onDelete }) {
  const hostname = (() => {
    try { return new URL(item.url).hostname; } catch { return item.site_name || "Website"; }
  })();

  return (
    <article className="preview-card">
      <div className="preview-image-wrap">
        {item.image_url
          ? <img className="preview-image" src={item.image_url} alt="" loading="lazy"
              onError={(event) => { event.currentTarget.style.display = "none"; }} />
          : <div className="image-placeholder"><span>↗</span></div>}
      </div>
      <div className="preview-content">
        <div className="site-line">
          {item.favicon_url && <img className="favicon" src={item.favicon_url} alt="" onError={(e) => e.currentTarget.style.display = "none"} />}
          <span>{item.site_name || hostname}</span>
        </div>
        <h3>{item.title || hostname}</h3>
        <p className="preview-description">{item.description || "No description available."}</p>
        <div className="card-footer">
          <a href={item.url} target="_blank" rel="noopener noreferrer">Visit website ↗</a>
          <button className="delete-button" onClick={() => onDelete(item.id)} aria-label="Delete saved URL">Delete</button>
        </div>
      </div>
    </article>
  );
}
