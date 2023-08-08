import axios from 'axios';
import React, { useState } from 'react'
import { Button } from 'react-bootstrap'
import useAxiosPrivate from '../hooks/useAxiosPrivate'
import { useNavigate, useLocation } from "react-router-dom"


const ImportLocal = () => {
  const [selectedFiles, setSelectedFiles] = useState(null)
  const axiosPrivate = useAxiosPrivate()
  const nav = useNavigate();
  const location = useLocation();

  const onFileChange = event => {
    setSelectedFiles(event.target.files);
  };

  const onFileUpload = () => {
    if (!selectedFiles) return false;
    const filesData = new FormData()
    const ins = selectedFiles.length;
    for (let x = 0; x < ins; ++x) {
      filesData.append('files[]', selectedFiles[x])
    }

    axiosPrivate.post("/uploadFilesLocal", filesData, {})
      .then(res => {
        alert(res.data.msg)
        window.location.reload();
      })
      .catch(res => {
        console.log(res);
        setSelectedFiles(null);
        nav("/", { state: { from: location }, replace: true });
      })
  };

  return (
    <div className='localUpload'>
      <input type="file" onChange={onFileChange} multiple />
      <Button variant="outline-warning" onClick={onFileUpload} size="sm">Upload</Button>
    </div>

  )
}

export default ImportLocal
