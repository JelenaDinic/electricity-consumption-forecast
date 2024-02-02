import { Button } from "@mui/material";
import React, { useState, ChangeEvent } from "react";

function Uploading() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
  };

  const handleUpload = () => {
    // Add your upload logic here, e.g., send the file to a server

    // For demonstration purposes, log the selected file details
    if (selectedFile) {
      console.log("Selected File:", selectedFile.name);
      console.log("File Size:", selectedFile.size);
      console.log("File Type:", selectedFile.type);
    } else {
      console.log("No file selected.");
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <Button
        style={{
          background:
            "linear-gradient(0deg, rgba(238,174,202,1) 0%, rgba(148,187,233,1) 100%)",
          fontSize: "22px",
          letterSpacing: "5px",
          marginTop: "10px",
        }}
        type="submit"
        variant="contained"
        color="secondary"
        fullWidth
        onClick={handleUpload}
      >
        Upload
      </Button>
    </div>
  );
}

export default Uploading;
