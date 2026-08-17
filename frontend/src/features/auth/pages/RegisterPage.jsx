import RegisterForm from "../components/RegisterForm";
import Container from "../../../shared/components/Container/Container";
import "./RegisterPage.scss";

function RegisterPage() {
  return (
    <Container>
      <main className="register-page">
        <h1 className="register-page__title">Register Page</h1>
        <RegisterForm />
      </main>
    </Container>
  );
}

export default RegisterPage;
