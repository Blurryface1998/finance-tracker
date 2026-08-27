import { useState } from "react";
import { getTransactions } from "../services/transactionService";

export function useTransaction() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTranasactions = async (filters = {}) => {
    try {
      setLoading(false);
      setError(null);

      const data = await getTransactions(filters);

      setTransactions(data.items);

      return data;
    } catch (err) {
      console.error("Failed to fetch transactions:", err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };
  return {
    transactions,
    loading,
    error,
    fetchTranasactions,
  };
}
