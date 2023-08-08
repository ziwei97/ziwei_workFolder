import React, { useState } from 'react'
import { Button } from 'react-bootstrap'
import useAxiosPrivate from '../hooks/useAxiosPrivate'
import { useNavigate, useLocation } from "react-router-dom"
import useAuth from '../hooks/useAuth'

const ReportCell = ({ cell }) => {
  const [selectedFiles, setSelectedFiles] = useState(null)

  const object_id = cell['row']['original']['_id']
  const report_num = cell['row']['original']['report']
  const nav = useNavigate();
  const location = useLocation();
  const axiosPrivate = useAxiosPrivate();
  const { auth, setAuth } = useAuth();

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
    filesData.append('object_id', object_id)

    axiosPrivate.post("/uploadReport", filesData, {})
      .then(res => {
        alert(res.data.msg)
        window.location.reload();
      })
      .catch(res => {
        console.log(res);
        setSelectedFiles(null)
        nav("/", { state: { from: location }, replace: true });
      })
  };

  const downloadReport = () => {
    axiosPrivate.get("/downloadReport/" + object_id, {
      responseType: "blob",
    }).then(res => {
      const blob = new Blob([res['data']], { type: 'application/pdf' })
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `report-${+new Date()}.pdf`;
      link.click();
    }).catch(res => {
      console.log(res);
      nav("/", { state: { from: location }, replace: true });
    })
  }

  return (
    <div className='localUpload'>
      {report_num ? <Button variant="outline-warning" onClick={downloadReport} className="mb-3" size="sm">Download Report</Button> : null}
      {auth.roles === "admin" ?
        <>
          <input type="file" onChange={onFileChange} multiple />
          <Button variant="outline-warning" onClick={onFileUpload} size="sm">Upload</Button>
        </> : null}

    </div>

  )
}

export default ReportCell