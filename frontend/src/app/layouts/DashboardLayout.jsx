import { Outlet, useLocation } from "react-router-dom";
import OverviewHeader from "../../shared/components/OverviewHeader/OverviewHeader";
import Sidebar from "../../shared/components/Sidebar/Sidebar";
import { personalNavigation } from "../navigation/links";

function DashboardLayout() {
  const location = useLocation();
  const links = personalNavigation[location.pathname] ?? [];
  return (
    <>
      <OverviewHeader logoLink="/overview" links={links} />
      <Sidebar links={links} />
      <Outlet />
    </>
  );
}

export default DashboardLayout;
