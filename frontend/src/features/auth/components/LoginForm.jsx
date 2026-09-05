import { data, Form, Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useForm, set } from "react-hook-form";
import Container from "../../../shared/components/Container/Container";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import Eye from "../../../assets/eye.svg";
import FormField from "./FormField/FormField";
import { loginUser, getCurrentUser } from "../services/authService";
import { handleFormError } from "../../../shared/utils/errorMessages";
import { submitWithLoading } from "../../../shared/utils/formSubmit";
import Loader from "../../../shared/components/Loader/Loader";

import { useAuth } from "../hooks/useAuth";
import "./LoginForm.scss";

function LoginForm() {
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    setError,
    clearErrors,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    try {
      await submitWithLoading({
        request: () => login(data),
        setLoading: setIsLoading,
        clearErrors,
      });

      navigate("/overview");
    } catch (err) {
      const errorData = handleFormError(err, setError, data);

      if (errorData?.error?.code === "invalid_credentials") {
        setError("root.server", {
          type: "server",
          message: errorData.error.message,
        });
      }
    }
  };
  return (
    <>
      {isLoading && <Loader />}
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
    </>
  );
}

export default LoginForm;
