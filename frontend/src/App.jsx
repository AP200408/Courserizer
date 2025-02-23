import './App.css'
import Chatbot from './components/Chatbot/Chatbot';
import ContactUs from './components/ContactUs/ContactUs'
import Footer from './components/Footer/Footer';
import Home from './components/Home/Home'
import HowToUse from './components/HowToUse/HowToUse';
import About from './components/About/About';
import Service from './components/Service/Service'
import { Routes, Route } from "react-router-dom";
import Procedures from './components/Procedures/Procedures';

function App() {

  return (
    <div className="app-container">
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/procedures" element={<Procedures />} />
        <Route path="/Korsy" element={<Chatbot />} />
        <Route path="/howtouse" element={<HowToUse />} />
        <Route path="/contact" element={<ContactUs />} />
        <Route path="/services" element={<Service />} />
      </Routes>

    </div>
  );
}

export default App;
