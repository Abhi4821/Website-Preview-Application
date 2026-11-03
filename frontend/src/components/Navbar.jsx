import { Link, useNavigate } from "react-router-dom";

export default function Navbar({ user }) {
  const navigate = useNavigate();

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  }

  return (
    <header className="navbar">
      <Link className="brand" to="/dashboard">
        <span className="brand-mark">L</span>
        <span>LinkShelf</span>
      </Link>
      <div className="nav-right">
        {user && <span className="welcome">Hi, {user.full_name}</span>}
        <button className="button button-ghost button-small" onClick={logout}>Logout</button>
      </div>
    </header>
  );
}
