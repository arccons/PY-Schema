import React, {useState, useEffect, Component} from 'react';
import axios from 'axios';
import { ButtonUsage } from '../Components/MUI-Components';

const Home = (props) => {

  const [file, setFile] = useState();
  const [subject, setSubject] = useState("No Selection");
  const [table, setTable] = useState();
  const [uploadedFile, setUploadedFile] = useState();
  const [error, setError] = useState();
  const [subjectList, setSubjectList] = useState([]);
  const [loaded, setLoaded] = useState(false)
  const [success, setSuccess] = useState(true)

  useEffect (() => {
    if (!loaded) {
      axios.get("http://localhost:8000/getSubjectList")
      .then((response) => {
        console.log(response.data.SUBJECT);
        setSubjectList(response.data.SUBJECT);
        setLoaded(true)
        console.log(subjectList);
      })
      .catch((error) => {
        console.error("Error getting subject list: ", error);
        setError(error);
      });
    }
  });

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  function handleSubjectChange(event) {
    if (props.newSubject) {
      if (subjectList.includes(event.target.value))
        setError("Subject already in use.");
      else setSubject(event.target.value);
    }
    else setSubject(event.target.value);
  }

  function handleTableChange(event) {
    setTable(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const url = 'http://localhost:8000/processFile/';
    const formData = new FormData();
    formData.append('uploadedFile', file);
    formData.append('fileType', file.type);
    formData.append('subject', subject)
    if (props.newSubject) {
      formData.append('table', table)
    }
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
        document.getElementById("MainForm").reset();
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
        setError(error);
      });
  }

  return (
    <div className="App">
        <form id="MainForm" onSubmit={handleSubmit}>
          <h1>DB File Upload</h1>
          
          {!props.newSubject &&
            <>
            <center>
              <label htmlFor="subject">Choose a Subject: </label>
                <select id="subject" onChange={handleSubjectChange}><option key='0' value="No Selection">Pick One</option>
                  {subjectList.map((sL)=><option key={sL} value={sL}>{sL}</option>)}</select>
                <br></br>
            </center>
            </>}
          {props.newSubject && 
            <>
              <center>
                <label htmlFor="subject">Create a Subject: </label>
                  <input type="text" id="subject" required onChange={handleSubjectChange}/>
                  <br></br>
                  <label htmlFor="table">Table for the Subject: </label>
                  <input type="text" id="table" onChange={handleTableChange} required/>
              </center>
            </>
          }
          <center>
            <label htmlFor="file">Choose a File: </label>
            <input type="file" id="fileToUpload" onChange={handleFileChange}/>
            <br></br>
            <br></br>
            <button onSubmit={handleSubmit}>Upload</button>
            <br></br>
            <br></br>
            <text>[Dates will be stored in <b>YYYY-MM-DD</b> format]</text>
          </center>
        </form>
        {uploadedFile && <center><p><text alt="Uploaded content">File uploaded successfully</text></p></center>}
        {error && <p>Error uploading file: {error.message}</p>}
    </div>
  );
};

export default Home;
