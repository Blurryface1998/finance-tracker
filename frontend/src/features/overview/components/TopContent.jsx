import Card from "../../../shared/components/Card/Card";
import MasterCard from "../../../assets/credit-card-logos/Mastercard.svg";
import ArrowUpRight from "../../../assets/button-icons/arrow-up-right.svg";
import Arrow from "../../../assets/button-icons/Leftarrow.svg";
import "./TopContent.scss";
function TopContent() {
  return (
    <div className="container">
      <div className="container__article">
        <h1 className="container__title">Total Balance</h1>
        <Card className="container__card">
          <div className="container__header">
            <h2 className="container__balance">$240,399</h2>{" "}
            {/* Total balance */}
            <p type="button" className="container__accounts">
              All Accounts
            </p>
          </div>
          <div className="container__credit-card">
            {/* Moving credit cards */}
            <div className="container__account-type">
              <span className="container__card-type">Account Type</span>
              <h3>Credit Card</h3>
              <p>**** **** **** 2598</p>
            </div>
            <div className="container__logo-amount">
              <img src={MasterCard} alt="master card icon" />
              <div className="container__amount-button">
                <p>25000$</p> {/* Balacne on the credit card */}
                <button type="button">
                  <img src={ArrowUpRight} alt="arrow icon" />
                </button>
              </div>
            </div>
          </div>
          <div className="container__pagination">
            <button type="button">
              <img src={Arrow} alt="icon for left" />
              Previous
            </button>
            <div className="container__slider">
              <button className="dot"></button>
              <button className="dot"></button>
              <button className="dot"></button>
            </div>
            <button type="button">
              Next{" "}
              <img src={Arrow} alt="icon for right" className="arrow-right" />
            </button>
          </div>
        </Card>
      </div>
      <div className="container__article">
        <h1 className="container__title">Goals</h1>
        <Card className="container__card">
          <div className="conainter__header">
            <h2 className="container__goal">$20,000</h2> {/* Balance of goal */}
            <button type="button" className="container__change-goal">
              <img src="" alt="change goal icon" />
            </button>
            <span>may, 2023</span>
          </div>
          <div className="conatianer__main">
            <div className="container__target">
              <div>
                <img src="" alt="medal icon" />
                <span>Target Achived</span>
              </div>
              <p>$12,500</p> {/* see wjhere it comes from */}
            </div>
            <div className="container__target">
              <div>
                <img src="" alt="target icon" />
                <span>This month Target</span>
              </div>
              <p>$20,000</p> {/* see where it comes from */}
            </div>
            <div className="container__fuel">Testing</div>
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
