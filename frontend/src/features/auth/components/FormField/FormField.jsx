import "./FormField.scss";

function FormField({
  label,
  name,
  type = "text",
  placeholder = "",
  required = false,
  labelAction,
  eyeElement,
  className = "",
}) {
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
          type={type}
          placeholder={placeholder}
          required={required}
        />
        {eyeElement}
      </div>
    </div>
  );
}

export default FormField;
