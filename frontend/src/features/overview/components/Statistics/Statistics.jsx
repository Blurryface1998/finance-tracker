import Card from "../../../../shared/components/Card/Card";
import "./Statistics.scss";
function Statistics() {
  return (
    <div className="statistic">
      <h1 className="statistic__title">Statistics</h1>

      <Card className="statistic_card">
        <div className="statistic__card--header">
          <button className="comparison-button">
            Weekly Comparison
            <img src="" alt="icon for down" />
          </button>

          <div className="indicator">
            <div className="this">
              <div className="rectangle"></div>
              <span>This week</span>
            </div>
            <div className="this">
              <div className="rectangle last"></div>
              <span>Last week</span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default Statistics;
