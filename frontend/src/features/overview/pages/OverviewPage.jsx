import { useState, useEffect } from "react";
import { useAuth } from "../../auth/hooks/useAuth";
import { useTransaction } from "../../transactions/hooks/useTransaction";
import TopContent from "../components/TopContent";
import "./OverviewPage.scss";

const dummyTransactions = [
  {
    id: 1,
    description: "Groceries",
    amount: "450.00",
    category: "Food",
    transaction_type: "expense",
    created_at: "2026-08-27T09:30:00",
  },
  {
    id: 2,
    description: "Salary",
    amount: "120000.00",
    category: "Income",
    transaction_type: "income",
    created_at: "2026-08-26T10:00:00",
  },
  {
    id: 3,
    description: "Netflix",
    amount: "899.00",
    category: "Entertainment",
    transaction_type: "expense",
    created_at: "2026-08-25T18:20:00",
  },
  {
    id: 4,
    description: "Electricity Bill",
    amount: "7200.00",
    category: "Bills",
    transaction_type: "expense",
    created_at: "2026-08-24T12:15:00",
  },
  {
    id: 5,
    description: "Freelance Work",
    amount: "35000.00",
    category: "Income",
    transaction_type: "income",
    created_at: "2026-08-23T14:45:00",
  },
];

function OverviewPage() {
  const { user, loading } = useAuth();
  const { transactions } = useTransaction();

  if (loading) return <p>Loading data...</p>;

  return (
    <div>
      <TopContent />
    </div>
  );
}

export default OverviewPage;
