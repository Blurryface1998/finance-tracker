import Card from "../../../../shared/components/Card/Card";
import Arrow from "../../../../assets/button-icons/chevron-right.svg";
import Gamepad from "../../../../assets/category/gamepad-2.svg";
import "./RecentTransaction.scss";
import formatDate from "../../../../shared/utils/formatDate";
import { useState } from "react";
import ButtonLink from "../../../../shared/components/ButtonLink/ButtonLink";
function RecentTransaction({
  transactions = [],
  loading,
  transactionType,
  onTransactionTypeChange,
  openAddTransaction,
}) {
  const filters = [
    { label: "all", value: "all" },
    { label: "income", value: "income" },
    { label: "expenses", value: "expense" },
  ];
  if (loading) return <p>loading</p>;
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
          <button
            type="button"
            className={transactionType === "all" ? "active" : ""}
            onClick={() => onTransactionTypeChange("all")}
          >
            all
          </button>

          <button
            type="button"
            className={transactionType === "income" ? "active" : ""}
            onClick={() => onTransactionTypeChange("income")}
          >
            income
          </button>

          <button
            type="button"
            className={transactionType === "expense" ? "active" : ""}
            onClick={() => onTransactionTypeChange("expense")}
          >
            expense
          </button>
        </div>
        {transactions.length === 0 ? (
          <div className="transaction__card--no-transactions">
            <p>No transaction right now</p>
            <ButtonLink type="button" onClick={() => openAddTransaction(true)}>
              Add transaction
            </ButtonLink>
          </div>
        ) : (
          <div className="transaction__card--items">
            {transactions.slice(0, 5).map((transaction) => (
              <div key={transaction.description} className="item">
                <div className="item__details">
                  <img src={Gamepad} alt="" />
                  <div className="text">
                    <p>{transaction.description}</p>
                    <span>{transaction.category}</span>
                  </div>
                </div>
                <div className="item__amount">
                  <p>${transaction.amount}</p>
                  <span>{formatDate(transaction.created_at)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}

export default RecentTransaction;
