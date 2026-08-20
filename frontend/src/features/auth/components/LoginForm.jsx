import { useState } from "react";
import { data, Form, Link } from "react-router-dom";
import Container from "../../../shared/components/Container/Container";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import Eye from "../../../assets/eye.svg";
import FormField from "./FormField/FormField";
import "./LoginForm.scss";
import { loginUser } from "../services/authService";
import { useForm, set } from "react-hook-form";
import { formatServerError } from "../../../shared/utils/errorMessages";
import api from "../../../services/api/axios";

function LoginForm() {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    try {
      const response = await loginUser(data);

      alert("Login Scessful!");
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
      if (errorData.error?.code === "invalid_credentials") {
        setError("root.server", {
          type: "server",
          message: errorData.error.message,
        });
      }
    }
  };
  return (
    <form className="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <div className="form__content">
        <div className="form__inputs">
          <FormField
            label="Email Address"
            name="email"
            type="email"
            placeholder="email"
            required
            {...register("email")}
            errorMessage={errors.email}
          />

          <FormField
            label="Password"
            name="password"
            type="password"
            placeholder="******"
            required
            className="form__password"
            {...register("password")}
            errorMessage={errors.password}
            labelAction={
              <Link className="forgot-password" to="#">
                Forgot password?
              </Link>
            }
            showPasswordToggle
          />
        </div>
        <div className="form__action">
          <div className="error-message">
            {errors.root?.server && (
              <p className="form__error">{errors.root.server.message}</p>
            )}
          </div>
          <div className="remeber-checkbox">
            <label className="user-remember" htmlFor="remember">
              Keep me signed in
              <input type="checkbox" id="remember" />
              <span className="checkmark"></span>
            </label>
          </div>
          <ButtonLink type="submit" classname="login-button">
            Login
          </ButtonLink>
        </div>
      </div>
    </form>
  );
}

export default LoginForm;
