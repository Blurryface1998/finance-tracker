import LoginForm from "../components/LoginForm";
import Container from "../../../shared/components/Container/Container";
import "./LoginPage.scss";

function LoginPage() {
  return (
    <>
      <main className="login-page">
        <h1 className="login-page__title">Finance Tracker</h1>
        <LoginForm />
      </main>
    </>
  );
}

export default LoginPage;
