import { Link } from "react-router-dom";
import "./ButtonLink.scss";

function ButtonLink({
  children,
  to,
  variant = "header",
  classname = "",
  ...props
}) {
  return (
    <Link
      to={to}
      className={`btn-link btn-link--${variant} ${classname}`}
      {...props}
    >
      {children}
    </Link>
  );
}

export default ButtonLink;
