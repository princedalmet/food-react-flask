import React, { useEffect, useState } from "react";
import "./ExploreMenu.css";
import axios from 'axios';
import { menu_list } from "../../assets/assets";

const ExploreMenu = ({ category, setCategory }) => {
	const [menuItems, setMenuItems] = useState([]);
	
	//Fetch menu items from backend
	useEffect(() => {
    axios.get("http://localhost:5000/api/menu")
        .then(response => {
            setMenuItems(response.data);
        })
        .catch(error => {
            console.error("There was an error fetching the menu!", error);
        });
}, []);


  return (
    <div className="explore-menu" id="explore-menu">
      <h1>Explore Our Menu</h1>
      <p className="explore-menu-text">
        Choose from a diverse menu featuring a delectable array of dishes. Our
        mission is to satisfy your cravings and elevate your dining experience,
        one delicious meal at a time.
      </p>
      <div className="explore-menu-list">
        {menu_list.map((item, index) => {
          return (
            <div
              key={index}
              className="explore-menu-list-item"
              onClick={() =>
                setCategory((prev) =>
                  prev === item.menu_name ? "All" : item.menu_name
                )
              }
            >
              <img
                src={item.menu_image}
                className={category === item.menu_name ? "active" : ""}
                alt="menu_image"
              />
              <p>{item.menu_name}</p>
            </div>
          );
        })}
      </div>
      <hr />
    </div>
  );
};

export default ExploreMenu;
