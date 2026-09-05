import { useState, useEffect } from "react";
import { useAuth } from "../../auth/hooks/useAuth";
import { useTransaction } from "../../transactions/hooks/useTransaction";
import TopContent from "../components/TopContent/TopContent";
import RecentTransaction from "../components/RecentTransaction/RecentTransaction";
import Statistics from "../components/Statistics/Statistics";
import ExpensesBreakdown from "../components/ExpensesBreakdown/ExpensesBreakdown";
import Modal from "../../../shared/components/Modal/Modal";
import AddTransactionForm from "../components/AddTransactionForm/AddTransactionForm";
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
  {
    id: 6,
    description: "Freelance jos",
    amount: "35000.00",
    category: "Income",
    transaction_type: "income",
    created_at: "2026-08-23T14:45:00",
  },
];

function OverviewPage() {
  const [isAddTransactionOpen, setIsAddTransactionOpen] = useState(false);
  const { user, loading: authLoading } = useAuth();
  const {
    transactions,
    loading: transactionLoading,
    filters,
    error,
    fetchTransactions,
  } = useTransaction();
  const [transactionType, setTransactionType] = useState("all");

  const loadTransaction = () => {
    fetchTransactions(
      transactionType === "all" ? {} : { transaction_type: transactionType },
    );
  };
  useEffect(() => {
    if (!authLoading && user) {
      fetchTransactions(
        transactionType === "all" ? {} : { transaction_type: transactionType },
      );
    }
  }, [authLoading, user, transactionType]);

  if (authLoading) return <p>Loading data...</p>;

  return (
    <div className="overview">
      {isAddTransactionOpen && (
        <Modal onClose={() => setIsAddTransactionOpen(false)}>
          <AddTransactionForm
            onTransactionCreate={loadTransaction}
            onClose={() => setIsAddTransactionOpen(false)}
          />
        </Modal>
      )}
      <div className="overview__top">
        <TopContent />
      </div>
      <div className="overview__left">
        <RecentTransaction
          transactions={transactions}
          loading={transactionLoading}
          transactionType={transactionType}
          onTransactionTypeChange={setTransactionType}
          openAddTransaction={setIsAddTransactionOpen}
        />
      </div>
      <div className="overview__right-top">
        <Statistics />
      </div>
      <div className="overview__right-bottom">
        <ExpensesBreakdown />
      </div>
    </div>
  );
}

export default OverviewPage;
