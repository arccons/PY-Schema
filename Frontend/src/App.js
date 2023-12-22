import './App.css';
import React, {useState} from 'react';
import axios from 'axios';

function App() {

  const [file, setFile] = useState();
  const [subject, setSubj] = useState("No Selection");
  const [uploadedFile, setUploadedFile] = useState();
  const [error, setError] = useState();

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  function handleSubjChange(event) {
    setSubj(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const url = 'http://localhost:8000/processFile/';
    const formData = new FormData();
    formData.append('uploadedFile', file);
    formData.append('fileType', file.type);
    formData.append('subject', subject)
    console.log(file.type)
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      },
    };
    axios.post(url, formData, config)
      .then((response) => {
        console.log(response.data);
        setUploadedFile(file);
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
        setError(error);
      });
  }

  return (
    <div className="App">
        <form onSubmit={handleSubmit}>
          <h1>React File Upload</h1>
          <label htmlFor="subject">Choose a subject:  </label>
          <select id="subject" onChange={handleSubjChange}>
            <option value="No Selection">Pick One</option>
            <option value="IndiaElectric">IndiaElectric</option>
          </select>
          <br/>
          <input type="file" id="fileToUpload" onChange={handleFileChange}/>
          <button type="submit">Upload</button>
        </form>
        {uploadedFile && <img src={uploadedFile} alt="Uploaded content"/>}
        {error && <p>Error uploading file: {error.message}</p>}
    </div>
  );
}

export default App;
