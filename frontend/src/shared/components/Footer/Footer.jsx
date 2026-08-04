import Container from "../Container/Container";
import "./Footer.scss";

function Footer() {
  return (
    <footer className="footer">
      <Container>
        <div className="footer_content">
          <span className="footer_copyright">
            {"\u00A9"} {new Date().getFullYear()} Finance Tracker
          </span>
        </div>
      </Container>
    </footer>
  );
}

export default Footer;
