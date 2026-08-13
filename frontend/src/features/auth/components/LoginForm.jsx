import { Link } from "react-router-dom";
import Container from "../../../shared/components/Container/Container";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import Eye from "../../../assets/eye.svg";
import "./LoginForm.scss";
function LoginForm() {
  return (
    <form className="form">
      <div className="form__content">
        <div className="form__inputs">
          <div className="form__email">
            <label className="input-label" htmlFor="email">
              Email Address
            </label>
            <input type="email" id="email" placeholder="email" />
          </div>
          <div className="form__password">
            <div className="password-header">
              <label className="input-label" htmlFor="password">
                Password
              </label>
              <Link className="forgot-password" to="#">
                Forgot Password?
              </Link>
            </div>
            <button className="show-password">
              <img src={Eye} alt="" className="eye" />
            </button>
            <input type="password" id="password" placeholder="password" />
          </div>
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
