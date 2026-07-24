import Hero from "./components/Hero";
import Features from "./components/Features";
import Footer from "../../shared/components/Footer/Footer";

function LandingPage() {
  return (
    <>
      <main>
        <Hero />
        <Features />
      </main>
      <Footer />
    </>
  );
}

export default LandingPage;
