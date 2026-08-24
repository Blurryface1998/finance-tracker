import ChevronRight from "../../../assets/chevrons-right.svg";
import Bell from "../../../assets/Bell.svg";
import Notification from "../../../assets/Notification-icon.svg";
import Search from "../../../assets/Search.svg";
import HamburgerMenu from "../../../assets/hamburger-menu.svg";
import "./OverviewHeader.scss";

function OverviewHeader({ onMenuClick }) {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate() + 1).padStart(2, "0");

  const formatDate = `${dd} ${mm}, ${yyyy}`;

  return (
    <header className="overview-header">
      <div className="overview-header__user">
        <div className="overview-header__user-info">
          <h1 className="overview-header__user-name">Name and last name</h1>

          <div className="overview-header__date">
            <img
              src={ChevronRight}
              alt=""
              className="overview-header__date-icon"
            />
            <span>{formatDate}</span>
          </div>
        </div>

        <div className="overview-header__notifiaction">
          <button
            type="button"
            className="overview-header__notification--button"
          >
            <img src={Notification} alt="Notifiaction" />
          </button>
        </div>
      </div>

      <div className="overview-header__mobile-actions">
        <div className="hamburger">
          <button type="button" onClick={onMenuClick}>
            <img src={HamburgerMenu} alt="Hamburger Menu" />
          </button>
        </div>
        <div className="search">
          <button type="button">
            <img src={Search} alt="Search" />
          </button>
        </div>
      </div>

      <div className="overview-header__desktop-actions">
        <button type="button" className="overview-header__notification-button">
          <img src={Notification} alt="" />
        </button>

        <div className="overview-header__search">
          <input
            type="search"
            name="search"
            className="overview-header__search-input"
            placeholder="Search here"
          />
          <img
            src={Search}
            alt="Search icon"
            className="overview-header__search-icon"
          />
        </div>

        <div className="overview-header__actions"></div>
      </div>
    </header>
  );
}

export default OverviewHeader;
