import { Outlet } from "react-router-dom";
import OverviewHeader from "../../shared/components/OverviewHeader/OverviewHeader";
import Sidebar from "../../shared/components/Sidebar/Sidebar";
import { personalNavigation } from "../navigation/links";
import "./DashboardLayout.scss";
import { useState } from "react";
function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  return (
    <div className="dashboard-layout">
      <Sidebar links={personalNavigation} isOpen={sidebarOpen} />
      <div className="dashboard-layout__main">
        <OverviewHeader
          onMenuClick={() => setSidebarOpen((prev) => !prev)}
          isSidebarOpen={sidebarOpen}
          onSearchClick={() => setSearchOpen((prev) => !prev)}
          isSearchOpen={searchOpen}
        />

        <main className="dashboard-layout__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;
