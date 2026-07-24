import { Link } from "react-router-dom";
import logo from "../../../assets/logo.svg";
function Header({ logoLink = "/", links = [] }) {
  return (
    <header>
      <Link className="logo-link" to={logoLink}>
        <img src={logo} alt="Logo for Finance Tracker" />
      </Link>
      <nav className="navigation-links">
        {links.map((link) => (
          <Link key={link.path} to={link.path}>
            {link.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
export default Header;
