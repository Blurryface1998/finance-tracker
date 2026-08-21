import "./OverviewHeader.scss";

function OverviewHeader({ logoLink = "/overview", links = [] }) {
  return (
    <header>
      <h1>Name and last name</h1>
      <img src="something" alt="" />
      <span>some date</span>
      <input type="search" name="search" id="search" />
    </header>
  );
}

export default OverviewHeader;
