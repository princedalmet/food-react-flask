import React, { useState } from "react";
import Navbar from "./components/Navbar/Navbar";
import { Route, Routes, useNavigate } from "react-router-dom";
import Home from "./pages/Home/Home";
import Cart from "./pages/Cart/Cart";
import PlaceOrder from "./pages/PlaceOrder/PlaceOrder";
import Footer from "./components/Footer/Footer";
import LoginPopup from "./components/LoginPopup/LoginPopup";
import Register from "./components/Register/Register";  // Import Register component
import RestaurantList from "./components/RestaurantList/RestaurantList";
import FoodCard from "./components/FoodProfile copy/FoodCard";
import RestaurantProfile from "./components/RestaurantProfile/RestaurantProfile";
import RestaurantPage from "./components/Restaurant copy/Restaurant";
import ContactUs from "./components/ContactUs";
import UserProfile from "./components/UserProfile";
import Login from "./components/Login/Login";  // Import Login component

const App = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [isContactUsOpen, setOpenContactUs] = useState(false);
  const navigate = useNavigate();  // To handle redirection

  return (
    <>
      {showLogin ? <LoginPopup setShowLogin={setShowLogin} /> : <></>}
      <div className="app">
        <Navbar setShowLogin={setShowLogin} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/order" element={<PlaceOrder />} />
          <Route path="/restaurants" element={<RestaurantList />} />
          <Route path="/contact-us" element={<ContactUs />} />
          <Route path="/food/:id" element={<FoodCard />} />
          <Route path="/restaurant/:id" element={<RestaurantPage />} />
          <Route path="/user-profile" element={<UserProfile />} />
          <Route 
            path="/register" 
            element={<Register setShowLogin={setShowLogin} />} 
          />  {/* Added register route */}
          <Route 
            path="/login" 
            element={<Login setShowLogin={setShowLogin} />} 
          />  {/* Added login route */}
        </Routes>
      </div>
      <Footer />
    </>
  );
};

export default App;
