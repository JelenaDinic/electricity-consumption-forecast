import React, { useState } from "react";
import axios from "axios";
import {
  Button,
  TextField,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
} from "@mui/material";

function Prediction() {
  const [selectDate, setSelectDate] = useState<string>("");
  const [numberDays, setNumberDays] = useState<string>("");
  const [predictionResult, setPredictionResult] = useState<number[]>([]);

  const apiUrl = "http://localhost:5000/api/predict_model";

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const requestData = {
      select_date: selectDate,
      number_days: numberDays,
    };

    try {
      const response = await axios.post(apiUrl, requestData);

      if (response.status === 200) {
        setPredictionResult(response.data.message);
      } else {
        alert("Failed to make prediction.");
      }
    } catch (error) {
      alert("Error during prediction: " + error);
    }
  };

  const generateTableRows = () => {
    const rows = [];
    const startDate = new Date(selectDate);

    for (let i = 0; i < predictionResult.length; i++) {
      const date = new Date(startDate);
      date.setHours(date.getHours() + i - 2);

      rows.push(
        <TableRow key={i}>
          <TableCell style={{ textAlign: "center" }}>{i + 1}</TableCell>
          <TableCell style={{ textAlign: "center" }}>
            {date.toLocaleString()}
          </TableCell>
          <TableCell style={{ textAlign: "center" }}>
            {predictionResult[i]}
          </TableCell>
        </TableRow>
      );
    }

    return rows;
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Select Date"
          type="date"
          variant="outlined"
          fullWidth
          value={selectDate}
          onChange={(e) => setSelectDate(e.target.value)}
          InputLabelProps={{
            shrink: true,
          }}
          margin="normal"
        />
        <TextField
          label="Number of Days"
          type="number"
          variant="outlined"
          fullWidth
          value={numberDays}
          onChange={(e) => setNumberDays(e.target.value)}
          margin="normal"
          inputProps={{ max: 7 }}
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
          color="secondary"
          fullWidth
        >
          Predict
        </Button>
      </form>

      {predictionResult.length > 0 && (
        <Paper style={{ maxHeight: 400, overflow: "auto", marginTop: "20px" }}>
          <Table
            style={{
              background:
                "radial-gradient(circle, rgba(238,174,202,1) 0%, rgba(148,187,233,1) 100%)",
            }}
            stickyHeader
            aria-label="sticky table"
          >
            <TableHead>
              <TableRow>
                <TableCell
                  style={{
                    fontWeight: "bold",
                    background: "#F3D7CA",
                    textAlign: "center",
                  }}
                >
                  Id
                </TableCell>
                <TableCell
                  style={{
                    fontWeight: "bold",
                    background: "#F3D7CA",
                    textAlign: "center",
                  }}
                >
                  Date Time
                </TableCell>
                <TableCell
                  style={{
                    fontWeight: "bold",
                    background: "#F3D7CA",
                    textAlign: "center",
                  }}
                >
                  Load
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>{generateTableRows()}</TableBody>
          </Table>
        </Paper>
      )}
    </div>
  );
}

export default Prediction;
