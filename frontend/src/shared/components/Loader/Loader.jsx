import "./Loader.scss";
import { useEffect } from "react";

function Loader() {
  useEffect(() => {
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = "";
    };
  }, []);
  return (
    <div className="loader-overlay">
      <div className="loader" />
    </div>
  );
}

export default Loader;
