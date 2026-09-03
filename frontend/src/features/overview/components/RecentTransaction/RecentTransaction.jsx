import Card from "../../../../shared/components/Card/Card";
import Arrow from "../../../../assets/button-icons/chevron-right.svg";
import Gamepad from "../../../../assets/category/gamepad-2.svg";
import "./RecentTransaction.scss";

function RecentTransaction() {
  return (
    <div className="transaction">
      <div className="transaction__header">
        <h2>Recent Transaction</h2>
        <button>
          View all <img src={Arrow} alt="" />
        </button>
      </div>
      <Card className="transaction__card">
        <div className="transaction__card--header">
          <button className="active">All</button>
          <button>Income</button>
          <button>Expenses</button>
        </div>
        <div className="transaction__card--items">
          <div className="item">
            <div className="item__details">
              <img src={Gamepad} alt="" />
              <div className="text">
                <p>Keyboard</p>
                <span>Gadget and gear</span>
              </div>
            </div>
            <div className="item__amount">
              <p>$22.00</p>
              <span>17 may 2023</span>
            </div>
          </div>

          <div className="item">
            <div className="item__details">
              <img src={Gamepad} alt="" />
              <div className="text">
                <p>Keyboard</p>
                <span>Gadget and gear</span>
              </div>
            </div>
            <div className="item__amount">
              <p>$22.00</p>
              <span>17 may 2023</span>
            </div>
          </div>

          <div className="item">
            <div className="item__details">
              <img src={Gamepad} alt="" />
              <div className="text">
                <p>Keyboard</p>
                <span>Gadget and gear</span>
              </div>
            </div>
            <div className="item__amount">
              <p>$22.00</p>
              <span>17 may 2023</span>
            </div>
          </div>

          <div className="item">
            <div className="item__details">
              <img src={Gamepad} alt="" />
              <div className="text">
                <p>Keyboard</p>
                <span>Gadget and gear</span>
              </div>
            </div>
            <div className="item__amount">
              <p>$22.00</p>
              <span>17 may 2023</span>
            </div>
          </div>

          <div className="item">
            <div className="item__details">
              <img src={Gamepad} alt="" />
              <div className="text">
                <p>Keyboard</p>
                <span>Gadget and gear</span>
              </div>
            </div>
            <div className="item__amount">
              <p>$22.00</p>
              <span>17 may 2023</span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default RecentTransaction;
