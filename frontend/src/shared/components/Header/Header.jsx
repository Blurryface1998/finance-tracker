import { Link } from "react-router-dom";
import "./Header.scss";
import ButtonLink from "../ButtonLink/ButtonLink";
import logo from "../../../assets/logo.png";
function Header({ logoLink = "/", links = [] }) {
  return (
    <header className={"header"}>
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
            <ButtonLink
              variant="header"
              classname={link.type}
              key={link.path}
              to={link.path}
            >
              {link.label}
            </ButtonLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
export default Header;
