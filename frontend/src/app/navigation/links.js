export const landingLinks = [
  {
    label: "Register",
    path: "/register",
    type: "register",
  },
  {
    label: "Login",
    path: "/login",
    type: "login",
  },
];
export const registerLinks = [
  {
    label: "Login",
    path: "/login",
  },
];
export const loginLinks = [
  {
    label: "Register",
    path: "/register",
  },
];

export const publicNavigation = {
  "/": landingLinks,
  "/register": registerLinks,
  "/login": loginLinks,
};

export const overviewLinks = [
  {
    label: "Overview",
    path: "/overview",
  },
];

export const balancesLinks = [
  {
    label: "Balances",
    path: "/balances",
  },
];

export const transactionsLinks = [
  {
    label: "Transactions",
    path: "/transactions",
  },
];

export const billsLinks = [
  {
    label: "Bills",
    path: "/bills",
  },
];

export const expensesLinks = [
  {
    label: "Expenses",
    path: "/expenses",
  },
];

export const goalsLinks = [
  {
    label: "Goals",
    path: "/goals",
  },
];

export const settingsLinks = [
  {
    label: "Settings",
    path: "/settings",
  },
];

export const analyticsLinks = [
  {
    label: "Analytics",
    path: "/analytics",
  },
];

export const profileLinks = [
  {
    label: "Profile",
    path: "/profile",
  },
];

export const personalNavigation = [
  {
    "/overview": overviewLinks,
    "/balances": balancesLinks,
    "/transactions": transactionsLinks,
    "/bills": billsLinks,
    "/expenses": expensesLinks,
    "/goals": goalsLinks,
    "/analytics": analyticsLinks,
    "/profile": profileLinks,
    "/settings": settingsLinks,
  },
];
