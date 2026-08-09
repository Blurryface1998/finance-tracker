import Container from "../Container/Container";
import "./Footer.scss";

function Footer() {
  return (
    <footer className="footer">
      <Container>
        <div className="footer__content">
          <span className="footer__copyright">
            {"\u00A9"} {new Date().getFullYear()} Finance Tracker
          </span>
        </div>
      </Container>
    </footer>
  );
}

export default Footer;
