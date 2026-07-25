import HeroSection from "./components/Hero/HeroSection";
import FeaturesSection from "./components/Features/FeaturesSection";
import Footer from "../../shared/components/Footer/Footer";
function LandingPage() {
  return (
    <>
      <main>
        <HeroSection />
        <FeaturesSection />
      </main>
      <Footer />
    </>
  );
}

export default LandingPage;
