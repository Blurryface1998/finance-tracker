import HeroSection from "./components/Hero/HeroSection";
import FeaturesSection from "./components/Features/FeaturesSection";
import Footer from "../../shared/components/Footer/Footer";
import "./LandingPage.scss";

function LandingPage() {
  return (
    <>
      <main className="main">
        <HeroSection />
        <FeaturesSection />
      </main>
      <Footer />
    </>
  );
}

export default LandingPage;
