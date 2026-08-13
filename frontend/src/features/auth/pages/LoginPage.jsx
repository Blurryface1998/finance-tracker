import LoginForm from "../components/LoginForm";
import Container from "../../../shared/components/Container/Container";
import "./LoginPage.scss";

function LoginPage() {
  return (
    <Container>
      <main className="login-page">
        <h1 className="login-page__title">Finance Tracker</h1>
        <LoginForm />
      </main>
    </Container>
  );
}

export default LoginPage;
