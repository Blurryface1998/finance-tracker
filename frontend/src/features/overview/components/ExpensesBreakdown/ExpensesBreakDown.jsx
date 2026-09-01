import Card from "../../../../shared/components/Card/Card";

function ExpensesBreakDown() {
  return (
    <div className="breakdown">
      <div className="breakdown__header">
        <h1 className="breakdown__header--title">Expenses Breakdown</h1>
        <span>*compare to last month</span>
      </div>
      <Card className="breakdown__card">
        <div className="breakdown__card--top"></div>
        <div className="breakdown__card--botom"></div>
      </Card>
    </div>
  );
}

export default ExpensesBreakDown;
