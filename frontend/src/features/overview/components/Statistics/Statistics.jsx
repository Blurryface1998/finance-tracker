import Card from "../../../../shared/components/Card/Card";
import DownArrow from "../../../../assets/arrows/Down-arrow.svg";
import "./Statistics.scss";
function Statistics({ transactions }) {
  return (
    <div className="statistic">
      <h1 className="statistic__title">Statistics</h1>

      <Card className="statistic__card">
        <div className="statistic__card--header">
          <button className="comparison-button">
            Weekly Comparison
            <img src={DownArrow} alt="icon for down" />
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
