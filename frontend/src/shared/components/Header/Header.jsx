import { Link } from "react-router-dom";
import Container from "../Container/Container";
import "./Header.scss";
import logo from "../../../assets/logo.png";
function Header({ logoLink = "/", links = [] }) {
  return (
    <header className="header">
      <Container>
        <div className="header__content">
          <Link className="header__logo" to={logoLink}>
            <img
              className="header__image"
              src={logo}
              alt="Logo for Finance Tracker"
            />
          </Link>
          <nav className="header__navigation">
            {links.map((link) => (
              <Link
                className="header__navigation-link"
                key={link.path}
                to={link.path}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      </Container>
    </header>
  );
}
export default Header;
