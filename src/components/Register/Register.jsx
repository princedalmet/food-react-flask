import React, { useState } from "react";
import "./Register.css";
import { assets } from "../../assets/assets";
import axios from "axios";  // Import axios for API requests

const Register = ({ setShowLogin, setShowRegister }) => {
  const [role, setRole] = useState("customer");
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirmPassword: "",
    phone_number: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");  // Clear previous errors

    // Basic form validation
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/register", {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password,
        role: role,
      });

      if (response.status === 201) {
        setSuccess(true);  // Set success state to true
        setTimeout(() => {
          setShowRegister(false);  // Close register popup
          setShowLogin(true);  // Open login popup
        }, 2000);  // Redirect to login after 2 seconds
      }
    } catch (error) {
      setError(error.response?.data?.error || "Registration failed. Please try again.");
    }
  };

  return (
    <div className="login-popup">
      <form className="login-popup-container" onSubmit={handleSubmit}>
        <div className="login-popup-title">
          <h2>Sign Up</h2>
          <img
            src={assets.cross_icon}
            alt="cross_icon"
            onClick={() => setShowRegister(false)}
          />
        </div>
        <div className="login-popup-inputs">
          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            value={formData.first_name}
            onChange={handleInputChange}
            required
          />
          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={handleInputChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Your email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleInputChange}
            required
          />
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            required
          />
          <input
            type="tel"
            name="phone_number"
            placeholder="Phone Number (optional)"
            value={formData.phone_number}
            onChange={handleInputChange}
          />

          <div className="role-toggle">
            <label className="customer-label">
              <input
                type="radio"
                value="customer"
                checked={role === "customer"}
                onChange={() => setRole("customer")}
              />
              Customer
            </label>
            <label>
              <input
                type="radio"
                value="restaurant_owner"
                checked={role === "restaurant_owner"}
                onChange={() => setRole("restaurant_owner")}
              />
              Restaurant Owner
            </label>
          </div>
        </div>

        <button type="submit" className="register-button">
          Create Account
        </button>

        <div className="login-popup-condition">
          <input type="checkbox" required />
          <p>By continuing, I agree to the terms of use & privacy policy</p>
        </div>

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">Registration successful! Redirecting to login...</p>}

        <p>
          Already have an account?{" "}
          <span onClick={() => setShowLogin(true)}>Login here</span>
        </p>
      </form>
    </div>
  );
};

export default Register;
