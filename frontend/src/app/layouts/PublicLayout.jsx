import { Outlet, useLocation } from "react-router-dom";
import Header from "../../shared/components/Header/Header";
import { publicNavigation } from "../navigation/links";
function PublicLayout() {
  const location = useLocation();
  const links = publicNavigation[location.pathname] ?? [];

  return (
    <>
      <Header logoLink="/" links={links} />
      <Outlet />
    </>
  );
}

export default PublicLayout;
