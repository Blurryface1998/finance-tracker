import "./AddTransactionForm.scss";
import { createTransaction } from "../../../transactions/services/transactionService";
import ButtonLink from "../../../../shared/components/ButtonLink/ButtonLink";
import { submitWithLoading } from "../../../../shared/utils/formSubmit";
import { useState } from "react";
import { useForm } from "react-hook-form";
import Loader from "../../../../shared/components/Loader/Loader";
import { handleFormError } from "../../../../shared/utils/errorMessages";
function AddTransactionForm({ onTransactionCreate, onClose }) {
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    clearErrors,
    formState: { errors },
  } = useForm();

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
      console.error("Failed to create transaction:", err);
    }
  };

  return (
    <div className="addTransactionForm">
      {isLoading && <Loader />}
      <form onSubmit={handleSubmit(onSubmit)}>
        <label htmlFor="description">
          Description<span>*</span>:
        </label>
        <input
          type="text"
          placeholder="Add Description"
          {...register("description", {
            required: "Description is required",
          })}
        />
        {errors.description && <span>{errors.description.message}</span>}
        <label htmlFor="amount">
          Amount<span>*</span>:
        </label>
        <input
          type="text"
          placeholder="Add Amount"
          {...register("amount", {
            required: "Amount is required",
            min: { value: 0.01, message: "Amount must be greater than 0" },
          })}
        />
        {errors.amount && <span>{errors.amount.message}</span>}
        <label htmlFor="category">
          Category<span>*</span>:
        </label>
        <input
          type="text"
          placeholder="Add Category"
          {...register("category", { required: "Category is required" })}
        />
        {errors.category && <span>{errors.category.message}</span>}
        <label htmlFor="transaction_type">
          Select Type<span>*</span>:
        </label>
        <select
          {...register("transaction_type", {
            required: "Transaction type is required",
          })}
        >
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
        {errors.transaction_type && (
          <span>{errors.transaction_type.message}</span>
        )}
        <ButtonLink type="submit">Submit</ButtonLink>
      </form>
    </div>
  );
}

export default AddTransactionForm;
