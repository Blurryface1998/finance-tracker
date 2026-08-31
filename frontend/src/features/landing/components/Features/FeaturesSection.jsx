import "./FeaturesSection.scss";
import FeaturesCard from "../FeaturesCard/FeaturesCard";
import Container from "../../../../shared/components/Container/Container";

const features = [
  {
    title: "Authentication",
    description: "Secure JWT based login and registration",
  },
  {
    title: "Transactions",
    description: "Add, edit, and delete your transactions",
  },
  {
    title: "Analytics",
    description: "Understand your spending habits",
  },
  {
    title: "Filtering",
    description: "Quickly find transactions",
  },
  {
    title: "Pagination",
    description: "Efficiently browse large transaction lists",
  },
  {
    title: "Security",
    description: "Protected user data with JWT authentication",
  },
];

function FeaturesSection() {
  return (
    <section className="features">
      <div className="features__container">
        <h2 className="features__title">Features</h2>
        {features.map((feature) => (
          <FeaturesCard
            key={feature.title}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </section>
  );
}

export default FeaturesSection;
