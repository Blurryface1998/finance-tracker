import { Link } from "react-router-dom";
import "./HeroSection.scss";
import Container from "../../../../shared/components/Container/Container";

function HeroSection() {
  return (
    <section className="hero">
      <Container>
        <div className="hero__content">
          <h1 className="hero__title">Finance Tracker</h1>

          <p className="hero__subtitle">Track your money smarter</p>

          <p className="hero__description">
            Manage transactions, understand spending, and take control of your
            finances.
          </p>
        </div>
        <div className="hero__actions">
          <Link className="hero__button" to="/register">
            Register
          </Link>
        </div>
      </Container>
    </section>
  );
}

export default HeroSection;
