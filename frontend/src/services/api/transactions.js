import api from "./axios";

export const getTransactions = async ({
  transaction_type,
  category,
  min_amount,
  max_amount,
  limit = 20,
  cursor,
} = {}) => {
  const response = await api.get("/transactions", {
    params: {
      transaction_type,
      category,
      min_amount,
      max_amount,
      limit,
      cursor,
    },
  });

  return response.data;
};

export const getTransaction = async (transactionId) => {
  const response = await api.get(`/transactions/${transactionId}`);

  return response.data;
};

export const createTransaction = async (data) => {
  const response = await api.post("/transctions", data);

  return response.data;
};

export const updateTransaction = async (transactionId, data) => {
  const response = await api.put(`/transactions/${transactionId}`, data);

  return response.data;
};

export const patchTransaction = async (transactionId, data) => {
  const response = await api.patch(`/transactions/${transactionId}`, data);

  return response.data;
};

export const deleteTransaction = async (transactionId, data) => {
  const response = await api.delete(`/transactions/${transactionId}`, data);
};
