import { useState } from 'react';
import './ContactUs.css';
import Navbar from '../Navbar/Navbar';
import Footer from '../Footer/Footer';

const ContactUs = () => {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [status, setStatus] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setStatus('Your message has been sent successfully!');
        setFormData({ name: '', email: '', message: '' });
      } else {
        setStatus('There was an error sending your message. Please try again later.');
      }
    } catch (error) {
      setStatus('An error occurred. Please try again later.');
    }
  };

  return (<>
      <Navbar />
      <div className="container">
          <h2>Contact Us</h2>
          {status && <p className="status-message">{status}</p>}
          <form onSubmit={handleSubmit}>
              <div className="form-group">
              <label htmlFor="name">Your Name:</label>
              <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
              />
              </div>
              <div className="form-group">
              <label htmlFor="email">Your Email:</label>
              <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
              />
              </div>
              <div className="form-group">
              <label htmlFor="message">Message:</label>
              <textarea
                  id="message"
                  name="message"
                  rows="5"
                  value={formData.message}
                  onChange={handleChange}
                  required
              ></textarea>
              </div>
              <button type="submit" className="btn-primary">
              Submit
              </button>
          </form>
      </div>
      <Footer />
    </>
  );
};

export default ContactUs;
