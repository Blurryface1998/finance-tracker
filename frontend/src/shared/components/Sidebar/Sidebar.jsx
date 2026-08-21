import ButtonLink from "../ButtonLink/ButtonLink";
import logo from "../../../assets/logo.png";
import "./Sidebar.scss";

function Sidebar(links = []) {
  return (
    <div className="sidebar">
      <div className="sidebar__logo">
        <img src={logo} alt="Logo for Finance Tracker" />
      </div>
      <nav className="sidebar__navigation">
        {links.map((link) => (
          <ButtonLink
            variant="sidebar"
            classname={link.type}
            key={link.path}
            to={link.path}
          >
            {link.label}
          </ButtonLink>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;
