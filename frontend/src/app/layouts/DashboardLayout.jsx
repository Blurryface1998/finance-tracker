import { Outlet } from "react-router-dom";
import OverviewHeader from "../../shared/components/OverviewHeader/OverviewHeader";
import Sidebar from "../../shared/components/Sidebar/Sidebar";
import { personalNavigation } from "../navigation/links";
import "./DashboardLayout.scss";
import { useState } from "react";
import AddTransactionForm from "../../features/overview/components/AddTransactionForm/AddTransactionForm";
import Modal from "../../shared/components/Modal/Modal";
function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [isAddTransactionOpen, setIsAddTransactionOpen] = useState(false);
  return (
    <div className="dashboard-layout">
      <Sidebar links={personalNavigation} isOpen={sidebarOpen} />
      <div className="dashboard-layout__main">
        <OverviewHeader
          onMenuClick={() => setSidebarOpen((prev) => !prev)}
          isSidebarOpen={sidebarOpen}
          onSearchClick={() => setSearchOpen((prev) => !prev)}
          isSearchOpen={searchOpen}
          openAddTransaction={() => setIsAddTransactionOpen(true)}
        />

        <main className="dashboard-layout__content">
          <Outlet />
        </main>
        {isAddTransactionOpen && (
          <Modal onClose={() => setIsAddTransactionOpen(false)}>
            <AddTransactionForm
              onClose={() => setIsAddTransactionOpen(false)}
            />
          </Modal>
        )}
      </div>
    </div>
  );
}

export default DashboardLayout;
