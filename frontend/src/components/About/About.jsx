import React from "react";
import Navbar from "../Navbar/Navbar";
import Footer from "../Footer/Footer";
import "./About.css"

function About() {
    
      return (<>
          <Navbar />
          <div className="container">
            <h1 className="title" style={{textDecoration:"underline", textUnderlineOffset:"0.3em"}}>About Us</h1>
            <div className="card">
              <p className="welcome ">
                Welcome to <span style={{textDecoration:"underline"}}>Courserizer</span> – Your AI-powered personal learning assistant! Our mission
                is to help students achieve their academic goals with smart time management,
                interactive learning tools, and personalized study plans.
              </p>
              <p className="text">
                <strong>Time Management & Productivity:</strong> StudyBuddy ensures students make the best use of their
                time with AI-driven scheduling, goal tracking, and task prioritization. Our platform
                helps learners stay organized and focused on their studies.
              </p>
              <p className="text">
                <strong>Smart AI Summarizers:</strong> Our advanced AI can summarize PDFs, web pages, and YouTube videos,
                allowing students to grasp key insights quickly without having to go through lengthy materials.
              </p>
              <p className="text">
                <strong>Interactive Q&A Forum:</strong> Engage with peers and educators through our discussion forum.
                Ask questions, share knowledge, and get answers instantly from a community of learners.
              </p>
              <p className="text">
                <strong>Mock Tests & Performance Analysis:</strong> Prepare effectively with custom mock tests and detailed
                performance analytics. Identify strengths and areas for improvement with AI-generated insights.
              </p>
              <p className="text">
                <strong>Smart Lesson Planning:</strong> Get AI-powered personalized study plans that adapt to your learning
                pace, helping you efficiently cover topics and stay ahead of deadlines.
              </p>
              <p className="text">
                <strong>Pomodoro Focus Mode:</strong> Improve concentration with StudyBuddy's Pomodoro mode, which enhances
                productivity by incorporating structured study and break intervals.
              </p>
            </div>
          </div>
          <Footer/>
        </>
      );
    };
    
export default About;
    