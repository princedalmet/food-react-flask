import React, { useState, useEffect } from "react";
import "./Login.css";
import { assets } from "../../assets/assets";
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
});

// Add response interceptor for handling 401s
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized errors
      localStorage.removeItem('user');
      // You might want to redirect to login or update app state here
    }
    return Promise.reject(error);
  }
);

const Login = ({ setShowLogin, setShowRegister, onLoginSuccess }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Check authentication status on component mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.get('/api/check-auth');
        if (response.data.authenticated) {
          onLoginSuccess(response.data.user);
          setShowLogin(false);
        }
      } catch (error) {
        console.log('Not authenticated');
      }
    };

    checkAuth();
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/login", {
        email,
        password,
      });

      console.log("Login response:", response.data);

      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
        onLoginSuccess(response.data.user);
        setShowLogin(false);
      }
    } catch (error) {
      console.error("Login error:", error);
      
      if (error.response) {
        // Server responded with error
        setError(error.response.data.error || "Invalid credentials");
      } else if (error.request) {
        // No response received
        setError("Server is not responding. Please try again later.");
      } else {
        // Request setup error
        setError("An error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-popup">
      <form className="login-popup-container" onSubmit={handleLogin}>
        <div className="login-popup-title">
          <h2>Login to Your Account</h2>
          <img
            src={assets.cross_icon}
            alt="close"
            onClick={() => setShowLogin(false)}
          />
        </div>
        <div className="login-popup-inputs">
          <input
            type="email"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        {error && (
          <div className="error-message" style={{ 
            color: 'red', 
            margin: '10px 0',
            padding: '8px',
            borderRadius: '4px',
            backgroundColor: '#ffebee'
          }}>
            {error}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading}
          style={{ opacity: loading ? 0.7 : 1 }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>

        <p className="register-link">
          Don't have an account?{" "}
          <span 
            onClick={() => {
              setShowLogin(false);
              setShowRegister(true);
            }}
            style={{ cursor: 'pointer', color: '#007bff' }}
          >
            Register here
          </span>
        </p>
      </form>
    </div>
  );
};

export default Login;