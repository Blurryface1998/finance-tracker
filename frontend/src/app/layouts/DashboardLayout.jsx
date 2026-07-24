import { Outlet } from "react-router-dom";

function DashboardLayout() {
  return (
    <>
      <h1>Dashboard Layout</h1>
      <Outlet />
    </>
  );
}

export default DashboardLayout;
