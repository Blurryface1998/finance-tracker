import { NavLink } from "react-router-dom";
import logo from "../../../assets/logo.png";
import Logout from "../../../assets/links/Logout.svg";
import "./Sidebar.scss";
import Profile from "../../../assets/links/Profile.svg";
function Sidebar({ links = [], isOpen }) {
  return (
    <aside className={`navbar ${isOpen ? "navbar--open" : ""}`}>
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
      <div className="navbar__footer">
        <a href="#" className="logout-button">
          <img src={Logout} alt="" />
          Logout
        </a>
        <div className="navbar__acount">
          <img src={Profile} alt="" />
          <div className="info">
            <p>Name and last name</p>
            <a href="/profile">View profile</a>
          </div>
          <button>
            <img src="#" alt="" />
          </button>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
