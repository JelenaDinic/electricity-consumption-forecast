import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";
import { Button, TextField } from "@mui/material";
import Prediction from "./components/Prediction";
import Training from "./components/Training";
import Uploading from "./components/Uploading";

function App() {
  return (
    <div>
      <h1
        style={{
          textAlign: "center",
          fontSize: "48px",
          fontFamily: "sans-serif",
          letterSpacing: "2px",
          color: "white",
        }}
      >
        Electricity Consumption Forecast
      </h1>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          padding: "30px",
        }}
      >
        <Uploading />
        <Training />
        <Prediction />
      </div>
    </div>
  );
}

export default App;
