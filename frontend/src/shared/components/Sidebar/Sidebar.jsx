import { NavLink } from "react-router-dom";
import logo from "../../../assets/logo.png";
import "./Sidebar.scss";

function Sidebar({ links = [] }) {
  return (
    <nav className="navbar">
      <div className="navbar__links">
        {links.map((link) => (
          <NavLink key={link.path} to={link.path} className="navbar__link">
            {link.icon && (
              <img src={link.icon} alt="" className="navbar__icon" />
            )}
            <span>{link.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

export default Sidebar;
