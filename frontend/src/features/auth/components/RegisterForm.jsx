import { Link } from "react-router-dom";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import "./RegisterForm.scss";
import FormField from "./FormField/FormField";
import Eye from "../../../assets/eye.svg";

function RegisterForm() {
  return (
    <form className="register">
      <div className="register__content">
        <FormField label="Name" name="name" placeholder="Name" required />

        <FormField
          label="Last Name"
          name="last-name"
          placeholder="Last name"
          required
        />

        <FormField
          label="Email"
          name="email"
          type="email"
          placeholder="name@example.com"
          required
        />

        <FormField
          label="Password"
          name="password"
          type="password"
          placeholder="*******"
          className="register__password"
          required
          eyeElement={
            <button className="show-password">
              <img src={Eye} alt="" />
            </button>
          }
        />

        <FormField
          label="Confirm Password"
          name="confirm-passowrd"
          type="password"
          placeholder="*******"
          required
          className="register__password"
          eyeElement={
            <button className="show-password">
              <img src={Eye} alt="" />
            </button>
          }
        />

        <div className="register__submit">
          <span className="terms">
            By continuing, you agree to our <Link>terms of service.</Link>
          </span>
          <ButtonLink classname="register-button">Register</ButtonLink>
        </div>
      </div>
    </form>
  );
}

export default RegisterForm;
