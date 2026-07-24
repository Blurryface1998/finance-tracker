import { Link } from "react-router-dom";

function Hero() {
  return (
    <section className="hero-section">
      <div className="hero-card">
        <h1 className="hero-title">Finance Tracker</h1>
        <h2 className="hero-explain">Track your money smarter</h2>
        <p className="hero-paragraph">
          Manage transactions, understand spending, and take control of your
          finances.
        </p>
      </div>
      <div className="hero-links">
        <Link className="hero-register" to="/register">
          Register
        </Link>
      </div>
    </section>
  );
}

export default Hero;
