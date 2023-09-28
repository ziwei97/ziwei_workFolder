import React, {useState, useEffect} from 'react';
import { Button, Table, Card, CardBody, CardHeader, Container} from 'reactstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../App.css'
import {Sidebar} from './Nav';
import { CiViewTable } from "react-icons/ci";


function Home() {

    const [DFUFileList, setDFUFileList] = useState([]);
    const [burnFileList, setBurnFileList] = useState([]);
    const itemsPerPage = 10;

    useEffect(() => {
      const fetchDFUData = async () => {
        axios.get('http://localhost:8000/api/cached-items/DFU').then((res) => {
          setDFUFileList(res.data.subfolders);
          console.log("DFU table loaded")
        }).catch((err) => console.log('Error fetching DFU file list:', err));
      };
      const fetchBurnData = async () => {
        axios.get('http://localhost:8000/api/cached-items/EPOC').then((res) => {
          setBurnFileList(res.data.subfolders);
          console.log("Burn table loaded")
        }).catch((err) => console.log('Error fetching Burn (EPOC) file list:', err));
      };
      fetchDFUData();
      fetchBurnData();
    }, []);

    
    const renderDataTableRows = (fileList) => {
    
      if (fileList.length === 0) {
        return (<div>Loading Data Table...</div>)
      }
  
      const indexOfLastItem = itemsPerPage;
      const indexOfFirstItem = indexOfLastItem - itemsPerPage;
      const currentItems = fileList.slice(indexOfFirstItem, indexOfLastItem);
  
      return currentItems.map((file) => {
        return (
          <tr key={file[0]}>
          <td className="truncate-cell">{file[0]}</td>
          <td className="truncate-cell">{file[1]}</td>
        </tr>
        )
      });
    };

    const DataCard = ({ header, linkTo, buttonColor, dataList }) => {
      const text = header.includes("DFU") ? "DFU" : "Burn";
      return (
        <Card>
          <CardHeader style={{ overflow: 'auto' }} className="d-flex justify-content-between align-items-center">
            <div className="truncate-cell"><span>{header}</span></div>
            <Link to={linkTo}>
              <Button className="auto-resizing-button" style={{background:"#155c07"}}><CiViewTable/> {`View All ${text} Data Files`}</Button>
            </Link>
          </CardHeader>
          <CardBody outline style={{ maxHeight: '100%', overflow: 'auto' }}>
            <Table className="transparent-table custom-table">
              <thead>
                <tr>
                  <th className="truncate-cell" style={{ width: '70%' }}>Data File Path</th>
                  <th className="truncate-cell" style={{ width: '30%' }}>Arrival Time to Local Server</th>
                </tr>
              </thead>
              <tbody>{renderDataTableRows(dataList)}</tbody>
            </Table>
          </CardBody>
        </Card>
      );
    };

    return (  
      <div style={{ display: 'flex', height: '100vh', overflow: 'scroll initial' }}>
        <Sidebar/>
        <div style={{ flex: 1, backgroundColor: '#eff5e6', maxWidth: '100%', overflowX: 'auto' }}>
          <h1 className="my-5 mx-5" style={{ color: '#424a2d' }}>Home</h1>
          <h4 className="my-5 mx-5" style={{ color: '#424a2d' }}>Local Server ip: 192.168.110.252</h4>
          <Container >
            <DataCard
              header="Latest DFU Data Files: 192.168.110.252/DFU"
              linkTo="/DFU_items"
              buttonColor="info"
              dataList={DFUFileList}
            />
            </Container>
            <br/>
            <Container >
              <DataCard
                header="Latest Burn Data Files: 192.168.110.252/EPOC"
                linkTo="/Burn_items"
                buttonColor="info"
                dataList={burnFileList}
              />
            </Container>
          <br/>
        </div>
        </div>
    );
}

export default Home;