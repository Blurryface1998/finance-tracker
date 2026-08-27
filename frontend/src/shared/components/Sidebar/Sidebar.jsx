import { NavLink } from "react-router-dom";
import Logo from "../../../assets/logo.png";
import Logout from "../../../assets/links/Logout.svg";
import Icon from "../../../assets/Icon.svg";
import Profile from "../../../assets/links/Profile.svg";
import { useAuth } from "../../../features/auth/hooks/useAuth";
import "./Sidebar.scss";
function Sidebar({ links = [], isOpen }) {
  const { user } = useAuth();
  return (
    <aside className={`navbar ${isOpen ? "navbar--open" : ""}`}>
      <div className="navbar__header">
        <h1 className="navbar__title">Finance Tracker</h1>
        <nav className="navbar__links">
          {links.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                isActive ? "navbar__link navbar__link--active" : "navbar__link"
              }
            >
              {link.icon && (
                <img src={link.icon} alt="" className="navbar__icon" />
              )}
              <span>{link.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="navbar__footer">
        <a href="#" className="logout-button">
          <img src={Logout} alt="" />
          Logout
        </a>
        <div className="navbar__profile">
          <div className="navbar__account">
            <img src={Profile} alt="" />
            <div className="info">
              <p>
                {user?.name} {user.last_name}
              </p>
              <a href="/profile">View profile</a>
            </div>
          </div>
          <img src={Icon} alt="" />
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
