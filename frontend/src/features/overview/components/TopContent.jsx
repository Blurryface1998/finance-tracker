import Card from "../../../shared/components/Card/Card";
import MasterCard from "../../../assets/credit-card-logos/Mastercard.svg";
import ArrowUpRight from "../../../assets/button-icons/arrow-up-right.svg";
import Arrow from "../../../assets/button-icons/chevron-right.svg";
import Edit from "../../../assets/button-icons/edit.svg";
import Award from "../../../assets/icons/Award.svg";
import Goal from "../../../assets/icons/octicon-goal.svg";
import "./TopContent.scss";
function TopContent() {
  return (
    <div className="container">
      <div className="container__article">
        <h1 className="container__title">Total Balance</h1>
        <Card className="container__card">
          <div className="container__card--details">
            <div className="container__card--details--header">
              <h2>$240,399</h2> {/* Total balance */}
              <p>All Accounts</p>
            </div>

            <div className="container__card--details--account-type">
              <div className="content">
                <span className="container__card-type">Account Type</span>

                <h3>Credit Card</h3>

                <p>**** **** **** 2598</p>
              </div>

              <div className="logo">
                <img src={MasterCard} alt="master card icon" />

                <div className="logo__amount-button">
                  <p>25000$</p> {/* Balacne on the credit card */}
                  <button type="button">
                    <img src={ArrowUpRight} alt="arrow icon" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="container__card--slider-options">
            <div className="previous">
              <img src={Arrow} alt="icon for left" className="arrow-right" />

              <button type="button" disabled>
                Previous
              </button>
            </div>

            <div className="slider">
              <button className="dot active"></button>

              <button className="dot"></button>

              <button className="dot"></button>
            </div>

            <div className="next">
              <button type="button">Next</button>

              <img src={Arrow} alt="icon for right" />
            </div>
          </div>
        </Card>
      </div>

      <div className="container__article">
        <h1 className="container__title">Goals</h1>
        <Card className="container__card">
          <div className="container__card--goals-header">
            <div className="goals-header">
              <h2>$20,000</h2> {/* Balance of goal */}
              <button type="button" className="container__change-goal">
                <img src={Edit} alt="change goal icon" />
              </button>
            </div>

            <span>may, 2023</span>
          </div>

          <div className="container__card--goals-details">
            <div className="left">
              <div className="left__target">
                <img src={Award} alt="Award icon" />
                <div>
                  <span>Target Achived</span>
                  <p>$12,500</p> {/* see wjhere it comes from */}
                </div>
              </div>

              <div className="left__target">
                <img src={Goal} alt="Goal icon" />
                <div>
                  <span>This month Target</span>
                  <p>$20,000</p> {/* see where it comes from */}
                </div>
              </div>
            </div>

            <div className="right">
              <div className="graph">
                <div></div>
                <div className="graph__target-range">
                  <span className="start">$0</span>
                  <span className="middle">12K</span>
                  <span className="end">$20K</span>
                </div>
              </div>
              <p>Target vs Achievement</p>
            </div>
          </div>
        </Card>
      </div>
      <div className="container__article">
        <div className="container__upper">
          <h1 className="container__title">Upcoming Bill</h1>
          <button type="button">
            View All <img src="" alt="right arow icon" />
          </button>
        </div>
        <Card className="contiainer__card">
          <div className="continaer__bill">
            <div className="contianer__date">
              <p>May</p>
              <p>15</p>
            </div>
            <div className="container__description">
              <h2>Figma</h2>
              <h3>Figma - Monthly</h3>
              <span>Last Charge - 14 may, 2022</span>
            </div>
            <div className="container__amount">
              <p>$150</p>
            </div>
          </div>
          <div className="container__bill">
            <div className="container__date">
              <p>May</p>
              <p>15</p>
            </div>
            <div className="container__description">
              <h2>Adobe</h2>
              <h3>Adobe - Yearly</h3>
              <span>Last Charge - 17, jun, 2023</span>
            </div>
            <div className="contianer__amount">
              <p>$559</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default TopContent;
