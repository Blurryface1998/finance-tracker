import { useState } from "react";
import "./FormField.scss";
import Eye from "../../../../assets/eye.svg";

function FormField({
  label,
  name,
  type = "text",
  placeholder = "",
  required = false,
  labelAction,
  showPasswordToggle = false,
  className = "",
  errorMessage,
  fieldRequirements = [],
  ...inputProps
}) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="form-field">
      <div className={`form-field__label-row ${className}`}>
        <label className="form-field__label" htmlFor={name}>
          {label}
        </label>
        {labelAction}
      </div>
      <div className={`form-field__input-row ${className}`}>
        <input
          className="form-field__input"
          id={name}
          name={name}
          type={type === "password" && showPassword ? "text" : type}
          placeholder={placeholder}
          required={required}
          {...inputProps}
        />
        {showPasswordToggle && type === "password" && (
          <button
            type="button"
            className="show-password"
            onClick={() => setShowPassword((prev) => !prev)}
          >
            <img
              src={Eye}
              alt={showPassword ? "Hide password" : "Show password"}
            />
          </button>
        )}
      </div>
      <div className="form-field__error-messages">
        {errorMessage && (
          <p className="form-field__error">{errorMessage.message}</p>
        )}
      </div>

      {fieldRequirements.length > 0 && (
        <div className="form-field__requirements">
          {fieldRequirements.map((requirement) => (
            <p
              key={requirement.text}
              className={
                requirement.valid
                  ? "form-field__requirement form-field__requirement--valid"
                  : "form-field__requirement"
              }
            >
              <span className="icons">{requirement.valid ? "✓" : "○"}</span>
              <span className="text">{requirement.text}</span>
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default FormField;
