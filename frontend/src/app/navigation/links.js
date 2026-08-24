import Bill from "../../assets/links/Bill.svg";
import Expencces from "../../assets/links/Expencces.svg";
import Goal from "../../assets/links/Goal.svg";
import Overview from "../../assets/links/Overview.svg";
import Settings from "../../assets/links/Settings.svg";
import Transaction from "../../assets/links/Transaction.svg";
import Wallet from "../../assets/links/wallet.svg";
import Analytics from "../../assets/links/Analytics.svg";
import Profile from "../../assets/links/Profile.svg";

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

export const overviewLinks = [];

export const balancesLinks = [];

export const transactionsLinks = [];

export const billsLinks = [];

export const expensesLinks = [];

export const goalsLinks = [];

export const settingsLinks = [];

export const analyticsLinks = [];

export const profileLinks = [];

export const personalNavigation = [
  {
    label: "Overview",
    path: "/overview",
    icon: Overview,
    alt: "Overview icon",
  },
  {
    label: "Balances",
    path: "/balances",
    icon: Wallet,
    alt: "Wallet icon",
  },
  {
    label: "Transactions",
    path: "/transactions",
    icon: Transaction,
    alt: "Transaction icon",
  },

  {
    label: "Bills",
    path: "/bills",
    icon: Bill,
    alt: "Bill icon",
  },
  {
    label: "Expenses",
    path: "/expenses",
    icon: Expencces,
    alt: "Expenses icon",
  },
  {
    label: "Goals",
    path: "/goals",
    icon: Goal,
    alt: "Goal icon",
  },
  {
    label: "Analytics",
    path: "/analytics",
    icon: Analytics,
    alt: "Analytics icon",
  },
  {
    label: "Profile",
    path: "/profile",
    icon: Profile,
    alt: "Profile icon",
  },
  {
    label: "Settings",
    path: "/settings",
    icon: Settings,
    alt: "Settings icon",
  },
];
