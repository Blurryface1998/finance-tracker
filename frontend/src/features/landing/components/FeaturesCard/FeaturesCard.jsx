import "./FeaturesCard.scss";

function FeaturesCard({ title, description }) {
  return (
    <article className="features-card">
      <h3 className="features-card__title">{title}</h3>
      <p className="features-card__description">{description}</p>
    </article>
  );
}

export default FeaturesCard;
