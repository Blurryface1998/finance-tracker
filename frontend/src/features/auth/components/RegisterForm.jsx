import { Link } from "react-router-dom";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import { registerUser } from "../services/authService";
import { formatServerError } from "../../../shared/utils/errorMessages";
import "./RegisterForm.scss";
import FormField from "./FormField/FormField";
import { useState } from "react";
import { set, useForm } from "react-hook-form";

function RegisterForm() {
  const {
    register,
    handleSubmit,
    setError,
    clearErrors,
    watch,
    formState: { errors },
  } = useForm();

  const password = watch("password", "");
  const passwordRequirements = {
    minLength: password.length >= 16,
    maxLength: password.length <= 128,
  };

  const confirmPassword = watch("confirm_password", "");
  const confirmPasswordRequirements = {
    matches: confirmPassword === password,
  };

  const name = watch("name", "");
  const nameRequirements = {
    minLength: name.length >= 1,
    maxLength: name.length <= 50,
  };
  const lastName = watch("last_name", "");
  const lastNameRequirements = {
    minLength: lastName.length >= 1,
    maxLength: lastName.length <= 100,
  };
  const email = watch("email", "");
  const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const onSubmit = async (data) => {
    const { confirm_password, ...userData } = data;
    try {
      await registerUser(userData);

      alert("Register Sucessful!");
    } catch (err) {
      const errorData = err.response?.data;
      if (!errorData) {
        console.error("Network or unexpected error:", err);
        return;
      }
      if (Array.isArray(errorData.detail)) {
        errorData.detail.forEach((error) => {
          const fieldName = error.loc[error.loc.length - 1];

          setError(fieldName, {
            type: "server",
            message: formatServerError(error.msg, fieldName, data),
          });
        });
      }
      if (errorData.error?.code === "email_registered") {
        setError("email", {
          type: "server",
          message: errorData.error.message,
        });
      }
    }
  };

  return (
    <form className="register" onSubmit={handleSubmit(onSubmit)} noValidate>
      <div className="register__content">
        <div className="register__inputs">
          <FormField
            label="Name"
            name="name"
            placeholder="Name"
            required
            {...register("name")}
            errorMessage={errors.name}
            fieldRequirements={[
              {
                text: "At least 1 charater",
                valid: nameRequirements.minLength,
              },
              {
                text: "No more then 50 characters",
                valid: nameRequirements.maxLength,
              },
            ]}
          />

          <FormField
            label="Last Name"
            name="last_name"
            placeholder="Last name"
            required
            {...register("last_name")}
            errorMessage={errors.last_name}
            fieldRequirements={[
              {
                text: "At least 1 character",
                valid: lastNameRequirements.minLength,
              },
              {
                text: "No more than 100 characters",
                valid: lastNameRequirements.maxLength,
              },
            ]}
          />

          <FormField
            label="Email"
            name="email"
            type="email"
            placeholder="name@example.com"
            required
            {...register("email")}
            errorMessage={errors.email}
            fieldRequirements={[
              {
                text: "Enter a valid email addres",
                valid: isValidEmail,
              },
            ]}
          />

          <FormField
            label="Password"
            name="password"
            type="password"
            placeholder="*******"
            className="register__password"
            required
            {...register("password")}
            showPasswordToggle
            errorMessage={errors.password}
            fieldRequirements={[
              {
                text: "At least 16 characters",
                valid: passwordRequirements.minLength,
              },
              {
                text: "No more then 128 characters",
                valid: passwordRequirements.maxLength,
              },
            ]}
          />

          <FormField
            label="Confirm Password"
            name="confirm_passowrd"
            type="password"
            placeholder="*******"
            className="register__password"
            showPasswordToggle
            {...register("confirm_password", {
              required: "Please confirm your password",
              validate: (value) =>
                value === password || "Passwords do not match",
            })}
            fieldRequirements={[
              {
                text: "Passwords must match",
                valid: confirmPasswordRequirements.matches,
              },
            ]}
          />
        </div>

        <div className="register__submit">
          <span className="terms">
            By continuing, you agree to our <Link>terms of service.</Link>
          </span>
          {errors.root?.server && (
            <p className="error-message">{errors.root.server.message}</p>
          )}
          <ButtonLink type="submit" classname="register-button">
            Register
          </ButtonLink>
        </div>
      </div>
    </form>
  );
}

export default RegisterForm;
