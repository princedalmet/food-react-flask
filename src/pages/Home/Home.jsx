import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import "./Home.css";
import Header from "../../components/Header/Header";
import ExploreMenu from "../../components/ExploreMenu/ExploreMenu";
import FoodDisplay from "../../components/FoodDisplay/FoodDisplay";
import RestaurantList from "../../components/RestaurantList/RestaurantList";
import Login from "../../components/Login/Login"; // Assuming your login component is here

const Home = () => {
  const [category, setCategory] = useState("All");
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Authentication state
  const [showLogin, setShowLogin] = useState(false); // For controlling login popup
  const navigate = useNavigate(); // For navigation

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    navigate("/home"); // Redirect to home page after login
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    navigate("/login"); // Redirect to login page after logout
  };

  return (
    <div>
      <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      {showLogin && <Login setShowLogin={setShowLogin} setShowRegister={setShowRegister} onLoginSuccess={handleLoginSuccess} />}
      <ExploreMenu category={category} setCategory={setCategory} />
      <FoodDisplay category={category} />
      <RestaurantList />
    </div>
  );
};

export default Home;
