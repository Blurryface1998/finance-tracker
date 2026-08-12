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
