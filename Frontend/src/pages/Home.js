import React, {useState, useEffect} from 'react';
import axios from 'axios';

const Home = (props) => {

  const [file, setFile] = useState();
  const [subject, setSubject] = useState("No Selection");
  const [table, setTable] = useState();
  const [uploadedFile, setUploadedFile] = useState();
  const [error, setError] = useState();
  const [subjectList, setSubjectList] = useState([]);
  const [loaded, setLoaded] = useState(false)

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
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
        setError(error);
      });
  }

  return (
    <div className="App">
        <form onSubmit={handleSubmit}>
          <h1>DB File Upload</h1>
          
          {!props.newSubject &&
            <>
              <label htmlFor="subject">Choose a Subject: </label>
              <select id="subject" onChange={handleSubjectChange}><option key='0' value="No Selection">Pick One</option>
                {subjectList.map((sL)=><option key={sL} value={sL}>{sL}</option>)}</select>
              <br></br>
            </>}
          {props.newSubject && 
            <>
              <label htmlFor="subject">Create a Subject: </label>
              <input type="text" id="subject" required onChange={handleSubjectChange}/>
              <br></br>
              <label htmlFor="table">Table for the Subject: </label>
              <input type="text" id="table" onChange={handleTableChange} required/>
              <br></br>
            </>
          }
          <label htmlFor="file">Choose a File: </label>
          <input type="file" id="fileToUpload" onChange={handleFileChange}/>
          <br></br>
          <button type="submit">Upload</button>
        </form>
        {uploadedFile && <img src={uploadedFile} alt="Uploaded content"/>}
        {error && <p>Error uploading file: {error.message}</p>}
    </div>
  );
};

export default Home;
