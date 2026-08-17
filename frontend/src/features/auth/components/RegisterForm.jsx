import { Link } from "react-router-dom";
import ButtonLink from "../../../shared/components/ButtonLink/ButtonLink";
import { registerUser } from "../services/authService";
import "./RegisterForm.scss";
import FormField from "./FormField/FormField";
import Eye from "../../../assets/eye.svg";

function RegisterForm() {
  async function handleSubmit(e) {
    e.preventDefault;
    const formData = new FormData(e.currentTarget);

    const userData = {
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
    };

    const response = await registerUser(userData);

    console.log(response); /* DELETE THIS! */
  }

  return (
    <form className="register" onChange={handleSubmit}>
      <div className="register__content">
        <div className="register__inputs">
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
        </div>

        <div className="register__submit">
          <span className="terms">
            By continuing, you agree to our <Link>terms of service.</Link>
          </span>
          <ButtonLink type="submit" classname="register-button">
            Register
          </ButtonLink>
        </div>
      </div>
    </form>
  );
}

export default RegisterForm;
