import React from "react";
import Navbar from "../Navbar/Navbar";
import Footer from "../Footer/Footer";
import "./Home.css"

function Home() {
    return(<>
        <Navbar />
        <div className="Hero">
            <h1>Home Page</h1>
        </div>
        <Footer />
    </>);
}

export default Home;