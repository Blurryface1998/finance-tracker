import "./AddTransactionForm.scss";
import { createTransaction } from "../../../transactions/services/transactionService";
import ButtonLink from "../../../../shared/components/ButtonLink/ButtonLink";
import { submitWithLoading } from "../../../../shared/utils/formSubmit";
import { useState } from "react";
import { useForm } from "react-hook-form";
import Loader from "../../../../shared/components/Loader/Loader";
function AddTransactionForm({ onTransactionCreate, onClose }) {
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, clearErrors } = useForm();

  const onSubmit = async (data) => {
    try {
      const response = await submitWithLoading({
        request: () => createTransaction(data),
        setLoading: setIsLoading,
        clearErrors,
      });
      onTransactionCreate();
      onClose();
      console.log(response);
    } catch (err) {
      console.error("Status:", err.response?.status);
      console.error("Response:", err.response?.data);
      console.error("Sent data:", data);
      throw err;
    }
  };

  return (
    <>
      {isLoading && <Loader />}
      <form onSubmit={handleSubmit(onSubmit)}>
        <label htmlFor="description">Description:</label>
        <input
          type="text"
          placeholder="Add Description"
          {...register("description")}
        />
        <label htmlFor="amount">Amount:</label>
        <input type="text" placeholder="Add Amount" {...register("amount")} />
        <label htmlFor="category">Category:</label>
        <input
          type="text"
          placeholder="Add Category"
          {...register("category")}
        />
        <label htmlFor="transaction_type">Select Type:</label>
        <select {...register("transaction_type")}>
          <option value="income">income</option>
          <option value="expense">expense</option>
        </select>
        <ButtonLink type="submit">Submit</ButtonLink>
      </form>
    </>
  );
}

export default AddTransactionForm;
