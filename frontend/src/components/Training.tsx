import React, { useState } from "react";
import axios from "axios";
import { Button, TextField } from "@mui/material";

function Training() {
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  const apiUrl = "http://localhost:5000/api/train_model";

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const requestData = {
      start_date: startDate,
      end_date: endDate,
    };

    try {
      const response = await axios.post(apiUrl, requestData);

      if (response.status === 200) {
        alert("Training is successfully finished!");
      } else {
        alert("Training failed.");
      }
    } catch (error) {
      alert("Error during training: " + error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField
        label="Start Date"
        type="date"
        variant="outlined"
        fullWidth
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        InputLabelProps={{
          shrink: true,
        }}
        margin="normal"
      />
      <TextField
        label="End Date"
        type="date"
        variant="outlined"
        fullWidth
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
        InputLabelProps={{
          shrink: true,
        }}
        margin="normal"
      />
      <Button
        style={{
          background:
            "linear-gradient(0deg, rgba(238,174,202,1) 0%, rgba(148,187,233,1) 100%)",
          fontSize: "22px",
          letterSpacing: "5px",
        }}
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
      >
        Start training
      </Button>
    </form>
  );
}

export default Training;
