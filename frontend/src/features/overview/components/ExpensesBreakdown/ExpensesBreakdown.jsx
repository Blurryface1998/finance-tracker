import Card from "../../../../shared/components/Card/Card";
import ArrowRight from "../../../../assets/arrows/arrow-right-1.svg";
import RedArrow from "../../../../assets/arrows/Up-arrow.svg";
import GreenArrow from "../../../../assets/arrows/Down-arrow-1.svg";
import Housing from "../../../../assets/category/Housing.svg";
import "./ExpensesBreakdown.scss";
function ExpensesBreakdown({ transactions }) {
  return (
    <div className="breakdown">
      <div className="breakdown__header">
        <h1 className="breakdown__header--title">Expenses Breakdown</h1>
        <span>*Compare to last month</span>
      </div>
      <Card className="breakdown__card">
        <div className="breakdown__card--all-items">
          <div className="components">
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Housing</span>
                    <p>$250.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>15%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Food</span>
                    <p>$350.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>08%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Transportation</span>
                    <p>$50.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>12%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
          </div>
          <div className="components">
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Entertainment</span>
                    <p>$80.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>15%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Shopping</span>
                    <p>$420.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>25%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
            <div className="components__item">
              <div className="components__item--icon">
                <img src={Housing} alt="" />
              </div>
              <div className="components__item--details">
                <div className="content">
                  <div className="content__name">
                    <span>Others</span>
                    <p>$650.00</p>
                  </div>
                  <div className="content__percentage">
                    <span>23%*</span>
                    <img src={RedArrow} alt="" />
                  </div>
                </div>
                <img src={ArrowRight} alt="" />
              </div>
            </div>
          </div>
          <img className="line" src="" alt="split line" />
        </div>
      </Card>
    </div>
  );
}

export default ExpensesBreakdown;
