import { Link } from "react-router-dom";
import "./HeroSection.scss";
import Container from "../../../../shared/components/Container/Container";
import ButtonLink from "../../../../shared/components/ButtonLink/ButtonLink";
import SplitLine from "../../../../assets/SplitLine.svg";
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

        <img className="hero__line" src={SplitLine} alt="" aria-hidden="true" />

        <div className="hero__actions">
          <ButtonLink variant="hero" to="/register">
            Register
          </ButtonLink>
        </div>
      </Container>
    </section>
  );
}

export default HeroSection;
