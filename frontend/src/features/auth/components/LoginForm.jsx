import { useState } from "react";
import { data, Form, Link } from "react-router-dom";
import Container from "../../../shared/components/Container/Container";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import Eye from "../../../assets/eye.svg";
import FormField from "./FormField/FormField";
import "./LoginForm.scss";
import { loginUser } from "../services/authService";
import { onSubmit } from "../hooks/useAuth";
function LoginForm() {
  const handleSubmit = (data) => {
    onSubmit(data, loginUser);
  };
  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="form__content">
        <div className="form__inputs">
          <FormField
            label="Email Address"
            name="email"
            type="email"
            placeholder="email"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
            required
          />

          <FormField
            label="Password"
            name="password"
            type="password"
            placeholder="******"
            required
            className="form__password"
            value={formData}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
            labelAction={
              <Link className="forgot-password" to="#">
                Forgot password?
              </Link>
            }
            eyeElement={
              <button className="show-password" type="button">
                <img src={Eye} className="eye" />
              </button>
            }
          />
        </div>
        <div className="form__action">
          <div>
            <label className="user-remember" htmlFor="remember">
              Keep me signed in
              <input type="checkbox" id="remember" />
              <span className="checkmark"></span>
            </label>
          </div>
          <ButtonLink classname="login-button">Login</ButtonLink>
        </div>
      </div>
    </form>
  );
}

export default LoginForm;
