import { Link } from "react-router-dom";
import "./ButtonLink.scss";

function ButtonLink({
  children,
  to,
  variant = "header",
  classname = "",
  type = "button",
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
    <button className={buttonClassName} type={type} {...props}>
      {children}
    </button>
  );
}

export default ButtonLink;
