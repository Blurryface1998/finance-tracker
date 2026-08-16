import { Form, Link } from "react-router-dom";
import Container from "../../../shared/components/Container/Container";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import Eye from "../../../assets/eye.svg";
import FormField from "./FormField/FormField";
import "./LoginForm.scss";
function LoginForm() {
  return (
    <form className="form">
      <div className="form__content">
        <div className="form__inputs">
          <FormField
            label="Email Address"
            name="email"
            type="email"
            placeholder="email"
            required
          />

          <FormField
            label="Password"
            name="password"
            type="password"
            placeholder="******"
            required
            className="form__password"
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
              Keep me sign in
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
