import React, {useState, useEffect} from 'react';
import axios from 'axios';

const Home = (props) => {

  const [file, setFile] = useState();
  const [subject, setSubject] = useState("No Selection");
  const [table, setTable] = useState();
  const [pageError, setPageError] = useState("");
  const [subjectList, setSubjectList] = useState([]);
  const [tableList, setTableList] = useState([]);
  const [gotSubjectList, setGotSubjectList] = useState(false);
  const [success, setSuccess] = useState(true);

  useEffect (() => {
    if (!gotSubjectList) {
      axios.get("http://localhost:8000/getSubjectList")
      .then((response) => {
        console.log(response.data.SUBJECTS, response.data.TABLE_NAMES);
        setSubjectList(response.data.SUBJECTS);
        setTableList(response.data.TABLE_NAMES);
        setGotSubjectList(true);
        console.log(subjectList, tableList);
      })
      .catch((error) => {
        console.error("Error getting subject list: ", error);
        setPageError(error);
      });
    }
  });

  function handleLoad(event) {
    document.getElementById("MainForm").reset();
    console.log("Form reset.")
  }

  function handleSubjectChange(event) {
    if (props.newSubject) {
      if (subjectList.includes(event.target.value)) {
        setPageError("Subject already in use.");
        document.getElementById("newSubjectError").innerHTML = "Subject already in use. Subjects: " + subjectList;
        console.log("Subject already in use. Subjects: " + subjectList);
      }
      else setSubject(event.target.value);
    }
    else setSubject(event.target.value);
  }

  function handleTableChange(event) {
    if (props.newSubject) {
      if (tableList.includes(event.target.value)) {
        setPageError("Table already in use.");
        document.getElementById("newTableError").innerHTML = "Table already in use. Tables: " + tableList;
        console.log("Table already in use. Tables: " + tableList);
      }
      else setTable(event.target.value);
    }
    else setTable(event.target.value);
  }

  function handleFileChange(event) {
    document.getElementById("newFileError").innerHTML = "";
    let newFile = event.target.files[0];
    console.log(newFile.type); //application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    if (["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"].includes(newFile.type)) {
      setFile(newFile);
    }
    else {
      setPageError("Unknown file type.");
      document.getElementById("newFileError").innerHTML = "Unknown file type: " + newFile.type;
      console.log("Unknown file type: " + newFile.type);
    }
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
        document.getElementById("MainForm").reset();
        setSuccess(response.data.message);
      })
      .catch((error) => {
        setPageError(error.message);
        console.error("Error uploading file: ", error.message);
      });
  }

  return (
    <div className="App">
        <form id="MainForm" onLoad={handleLoad} onSubmit={handleSubmit}>
          <center><h1>DB File Upload</h1></center>
          
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
                <label htmlFor="newSubject">Create a Subject: </label>
                  <input type="text" id="newSubject" required onChange={handleSubjectChange}/>
                  <p id="newSubjectError"></p>
                  <label htmlFor="newTable">Table for the Subject: </label>
                  <input type="text" id="newTable" onChange={handleTableChange} required/>
                  <p id="newTableError"></p>
              </center>
            </>
          }
          <center>
            <label htmlFor="fileToUpload">Choose a File: </label>
            <input type="file" id="fileToUpload" onChange={handleFileChange}/>
            <p>Only .csv and .xl* files allowed</p>
            <p id="newFileError"></p>
            <button onSubmit={handleSubmit}>Upload</button>
            <br></br>
            <p>[Dates will be stored in <b>YYYY-MM-DD</b> format]</p>
          </center>
        </form>
        {success && <center>{success}</center>}
        {pageError && <center>{pageError}</center>}
    </div>
  );
};

export default Home;
