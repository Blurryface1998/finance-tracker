import { Outlet, useLocation } from "react-router-dom";
import OverviewHeader from "../../shared/components/OverviewHeader/OverviewHeader";
import Sidebar from "../../shared/components/Sidebar/Sidebar";
import { personalNavigation } from "../navigation/links";

function DashboardLayout() {
  const location = useLocation();
  return (
    <>
      <OverviewHeader />
      <Sidebar links={personalNavigation} />
      <Outlet />
    </>
  );
}

export default DashboardLayout;
