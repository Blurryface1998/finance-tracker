import { Link } from "react-router-dom";
import "./ButtonLink.scss";

function ButtonLink({
  children,
  to,
  variant = "header",
  classname = "",
  type = "button",
  disabled,
  ...props
}) {
  const buttonClassName = `btn-link btn-link--${variant} ${classname}`;
  if (to) {
    return (
      <Link to={to} className={buttonClassName} {...props}>
        {children}
      </Link>
    );
  }
  return (
    <button
      className={buttonClassName}
      type={type}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}

export default ButtonLink;
