import React, { useState, useEffect } from 'react';
import { Button,
  Card, CardBody, CardHeader, CardFooter, CardText, CardTitle,
  Table, Container,
  Navbar, Nav, NavItem, NavLink,
  Pagination, PaginationItem, PaginationLink, Badge,
  PopoverHeader, PopoverBody, UncontrolledPopover,
  Row, Col} from 'reactstrap';
import axios from 'axios';
import '../App.css';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {Sidebar} from './Nav';
import { FaFileDownload, FaCopy } from 'react-icons/fa';
import { IoMdOptions } from "react-icons/io";
import DataPieChart from './DataPieChart';


function ItemDetailPage () {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [selectedNavItem, setSelectedNavItem] = useState('Data Transfer Info');
  const [fieldNames, setFieldNames] = useState(['path', 'data_acquisition_time_range', 
  'data_transfer_date', 
  'spectral_view_size_on_drive', 
  'Pictures_size_on_drive']);
  const [guidNames, setGuidNames] = useState([]);
  const [guids, setGuids] = useState([]);
  // const [guidTableRows, setGuidTableRows] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedGUIDColumn, setSelectedGUIDColumn] = useState('Image Collection Folder Name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredItems, setFilteredItems] = useState(guidNames.map((name, index) => ({ name, id: guids[index] })));
  const itemsPerPage = 5;
  const [patientIDList, setPatientIDList] = useState("");
  const [typeCountList, setTypeCountList] = useState("");
  const [pieData, setPieData] = useState([]);
  const [dataIssues, setDataIssues] = useState({"Data Transfer Info": new Set(), "Collection Info": new Set(), "Images Categorization": new Set(), "Patients Stat": new Set()}); 

  // The following useState is for search option
  const [showSearchForm, setShowSearchForm] = useState(false);
  const [popoverOpen, setPopoverOpen] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState("All");

  // copy path use state
  const [copied, setCopied] = useState(false);

  // for the diff
  const [imageCollNotInDrive, setImageCollNotInDrive] = useState([]);
  const [imageCollNotInExcel, setImageCollNotInExcel] = useState([]);

  const toggleSearchForm = () => {
    setShowSearchForm(!showSearchForm);
  };

  const togglePopover = () => {
    setPopoverOpen(!popoverOpen);
  }

  const getFilteredItems = (items, searchTerm) => {
    return items.filter((item) => {
      const rowData = item.name + item.id; // Adjust as per your column data
      return rowData.toLowerCase().includes(searchTerm.toLowerCase());
    });
  };

  const calculateTotalPages = (items, itemsPerPage) => {
    return Math.ceil(items.length / itemsPerPage);
  };

  const sortAndFilter = (names, ids, column, order, searchTerm) => {
    const sortedItems = sortedGUIDData(names, ids, column, order);
    const filteredItems = getFilteredItems(sortedItems, searchTerm);
    setFilteredItems(filteredItems);
    const newTotalPages = calculateTotalPages(filteredItems, itemsPerPage);
    setTotalPages(newTotalPages);
    setCurrentPage(1);
    return filteredItems;
  };

  const handleGUIDColumnClick = (column) => {
    if (selectedGUIDColumn === column) {
      // If the same column is clicked again, reverse the sort order
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      // If a different column is clicked, update the sort column and set the initial sort order
      setSelectedGUIDColumn(column);
      setSortOrder('asc');
    }
  };

 
  const sortedGUIDData = (names, ids, column, order) => {
    // Combine the names and ids arrays into an array of objects
    const data = names.map((name, index) => ({ name, id: ids[index] }));
    // Sort the data based on the selected column and sort order
    if (selectedGUIDColumn === 'Image Collection Folder Name') {
      data.sort((a, b) => {
        return sortOrder === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
      });
    } else if (selectedGUIDColumn === 'GUID') {
      data.sort((a, b) => {
        return sortOrder === 'asc' ? a.id.localeCompare(b.id) : b.id.localeCompare(a.id);
      });
    }
    return data;
  };
    
  const handleNavItemClick = (navItem) => {
    setSelectedNavItem(navItem);
    if (navItem === 'Collection Info') {
      setFieldNames(['name',
      'eq_number',
      'serial_id',
      'patient_count',
      'image_coll_count_in_drive',
      'image_coll_count_in_verification_excel',
      'is_match']);
    } else if (navItem === 'Images Categorization') {
      setFieldNames(['images_count',
      'Raw_MSI',
      'Pseudocolor_generation_intermediate_output',
      'Pseudocolor',
      'Reference', 
      'CJA']);
    } else if (navItem === 'Data Transfer Info') {
      setFieldNames(['path',
      'data_acquisition_time_range', 
      'data_transfer_date', 
      'spectral_view_size_on_drive', 
      'Pictures_size_on_drive']);
    } else {
      setFieldNames([]);
    }
  };

  
  useEffect(() => {
    const fetchItem = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/data_file_infos/${id}/`);
        const itemData = response.data;
        if (!itemData.is_match) {
          // Append the new error message to the already existing list dataIssues["Collection Info"] by calling setDataIssues
          setDataIssues(prevState => {
            const newDataIssues = { ...prevState }; // Create a shallow copy of the state object
            const collectionInfoSet = new Set(prevState["Collection Info"]); // Create a new Set from the existing array
            
            // Add the new issue to the Set
            collectionInfoSet.add("Image collection count in drive does not match image collection count in verification excel");
            
            newDataIssues["Collection Info"] = collectionInfoSet; // Update the property with the modified Set
            return newDataIssues; // Update the state with the modified object
          });
        }
        console.log(itemData);
        setItem(itemData);
        if (response.data.images_in_excel_without_overlap !== '') {
          const images_in_excel_without_overlap = response.data.images_in_excel_without_overlap.split(',');
          setImageCollNotInDrive(images_in_excel_without_overlap);
        }
        if (response.data.images_in_drive_without_overlap !== '') {
          const images_in_drive_without_overlap = response.data.images_in_drive_without_overlap.split(',');
          setImageCollNotInExcel(images_in_drive_without_overlap); 
        }
      } catch (error) {
        console.error("unable to fetch item: ", error);
      }
    };

    fetchItem();
  }, [id]);

  useEffect(() => {
    const renderGUIDList = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/guid_lists/${item.guidListID}/`);
        const names = response.data.ImageCollFolderNames.split(',');
        const guids = response.data.ImgCollGUIDs.split(',');

        setGuidNames(names);
        setGuids(guids);
        sortAndFilter(names, guids, selectedGUIDColumn, sortOrder, searchTerm);
        // setTotalPages(Math.ceil(postFiltered.length / itemsPerPage));
      } catch (error) {
        console.error('There was an error aaaa!', error);
      }
    };
    const renderPatientsStat = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/patient_image_counts/${item.PatientImageCountID}/`);
        let pieData = []
        const patientIDs = response.data.patient_id_list.split(';');
        const typeCounts = response.data.image_count_list.split(';');
        for (let i = 0; i < patientIDs.length; i++) {
          const eachField = typeCounts[i].split(',');
          let total = 0;
          let lst = [];
          for (let j = 0; j < eachField.length; j++) {
            const eachType = eachField[j].split(':');
            eachType[1] = parseInt(eachType[1]);
            // add eachType as a pair to lst
            lst.push(eachType);
            total += parseInt(eachType[1]);
          }
          let dataDict = {name: patientIDs[i], total_img: total}
          for (let k = 0; k < lst.length; k++) {
            // if lst[k][1] is undefined, make it a string called "missing"
            dataDict[lst[k][0]] = lst[k][1];
          } 
          // Check potential issue with DataDict:
          checkPatientData(dataDict);
          pieData.push(dataDict)
          setPieData(pieData);
        }
        // console.log(patientIDs);
        setPatientIDList(patientIDs);
        // console.log(patientIDs);
        setTypeCountList(typeCounts);
      } catch (error) {
        console.error('There was an error aaaa!', error);
      }
    };
    renderPatientsStat();
    renderGUIDList();
  }, [id, item, searchTerm, sortOrder]);

  const setDataTransferIssue = (category, msg) => {
    setDataIssues(prevState => {
      const newDataIssues = { ...prevState }; // Create a shallow copy of the state object
      const categorySet = new Set(prevState[category]); // Create a new Set from the existing array in the category
  
      // Add the new message to the Set
      categorySet.add(msg);
  
      newDataIssues[category] = categorySet; // Update the property with the modified Set
      return newDataIssues; // Update the state with the modified object
    });
  };

  const checkPatientData = (dataDict) => {
    // if the data dictionary is missing the field "Pseudocolor" or "Raw_MSI", append to dataIssues with string "no PseudoColor in (patient number)" or "no Raw_MSI from (patient number)"
    if (!dataDict.hasOwnProperty("Pseudocolor")) {
      setDataTransferIssue("Patients Stat", `no PseudoColor in ${dataDict.name}`);
      // setDataIssues([...dataIssues, `no PseudoColor in ${dataDict.name}`]);
    } else if (!dataDict.hasOwnProperty("Raw_MSI")) {
      setDataTransferIssue("Patients Stat", `no Raw_MSI from ${dataDict.name}`);
      // setDataIssues([...dataIssues, `no Raw_MSI from ${dataDict.name}`]);
    } else if (dataDict.Pseudocolor * 20 < dataDict.Raw_MSI) {
      setDataTransferIssue("Patients Stat", `Missing PseudoColor in ${dataDict.name}`);
    } else if (dataDict.Pseudocolor * 20 > dataDict.Raw_MSI) {
      setDataTransferIssue("Patients Stat", `Missing Raw_MSI in ${dataDict.name}`);
        // setDataIssues([...dataIssues, `Missing Raw_MSI in ${dataDict.name}`]);
    }
  }

  if (!item || !guidNames || !guids) {
    return <div>Loading...</div>;
  }

  const renderGuidTableRows = (item) => {
    
    if (guidNames.length === 0 || guids.length === 0) {
      return (<div>Loading GUID list...</div>)
    }

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    // const currentItems = guidNames.slice(indexOfFirstItem, indexOfLastItem);
    // const currGuids = guids.slice(indexOfFirstItem, indexOfLastItem);
    const currSortedGUIDData = filteredItems.slice(indexOfFirstItem, indexOfLastItem);

    return currSortedGUIDData.map((dataItem, index) => {
      return (
        <tr key={index}>
        <td className="truncate-cell">{dataItem.name}</td>
        <td className="truncate-cell">{dataItem.id}</td>
      </tr>
      )
    });
  };

  const handleDownload = () => {
    // generate csv from States guidNames and guids
    if (guidNames !== [] && guids !== []) {
      // create csv files using guidNames and guids. Column names are Image Collection Folder Name and GUID
      const headerRow = ['Image Collection Folder Name', 'GUID'];
      const dataRows = guidNames.map((guidName, index) => [guidName, guids[index]]);
      const csvContent = `${headerRow.join(',')}\n${dataRows.map(row => row.join(',')).join('\n')}`;
      const csvData = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const downloadLink = document.createElement('a');
      const url = URL.createObjectURL(csvData);
      downloadLink.href = url;
      downloadLink.download = item.name + "_guidList.csv";
      downloadLink.click();
      URL.revokeObjectURL(url);
      downloadLink.remove();
    }
  }

  const handleCopyPathClick = () => {
    navigator.clipboard.writeText(item.path)
      .then(() => {
        console.log('Text copied to clipboard:', item.path);
        // You can add additional logic or UI updates here
        setCopied(true);
        setTimeout(() => {
          setCopied(false);
        }, 500); // Clear the message after 3 seconds
      })
      .catch((error) => {
        console.error('Failed to copy text to clipboard:', error);
      });
  };

  const handleDownloadVerificationInfo = () => {
    // print out dataIssues, pieData and item.data all into one big txt file
    // Store all the values in dataIssues, which is a dictionary into an array called dataIssuesValues

    const dataIssuetxtContent = `Immediate Issue(s): 
    ${combinedArray.length === 0? "No immediate issues found" :
    combinedArray.map((issue, index) => {
      return (
        // A list of issues
        `${index+1}. ${issue}`
      )
    })
    }`;

    console.log(imageCollNotInExcel);
    console.log(imageCollNotInDrive)
    let missingInDriveContent = imageCollNotInDrive.length === 0? "None" : 
    imageCollNotInDrive.map((item, index) => {
      return (
        // A list of issues
        `${index+1}. ${item}`
      )
    }).join('\n');
    missingInDriveContent = "The following image collections folder do not exist in hard drive: \n" + missingInDriveContent;

    let missingInExcelContent = imageCollNotInExcel.length === 0? "None" :
    imageCollNotInExcel.map((item, index) => {
      return (
        // A list of issues
        `${index+1}. ${item}`
      )
    }).join('\n');
    missingInExcelContent = "The following image collections are either entirely missing in Excel, or the AcquitionData.txt is missing: \n" + missingInExcelContent;

    const pieDatatxtContent = `Image Collections for Each Patient: \n${pieData.length === 0 ? "No patient stat found" :
    pieData.map((patient, index) => {
      return (
        // A list of issues
        `${index+1}. ${patient.name}: ${patient.total_img} images in total, ${patient.Raw_MSI} Raw MSI, ${patient.Pseudocolor_generation_intermediate_output} Pseudocolor_generation_intermediate_output, ${patient.Pseudocolor} Pseudocolor, ${patient.Reference} Reference, ${patient.CJA} CJA `
      )
    }).join('\n')
  }`;
    const itemDatatxtContent = `Data Transfer Info: 
    file_path: ${item.path}
    file_type: ${item.file_type}
    file_name: ${item.name}
    EQ_number: ${item.eq_number}
    serial_id: ${item.serial_id}
    patient_count: ${item.patient_count}
    image_coll_count_in_drive: ${item.image_coll_count_in_drive}
    image_coll_count_in_verification_excel: ${item.image_coll_count_in_verification_excel}
    data_acquisition_time_range: ${item.data_acquisition_time_range} 
    data_transfer_date: ${item.data_transfer_date}
    spectral_view_size_on_drive: ${item.spectral_view_size_on_drive}
    Pictures_size_on_drive: ${item.Pictures_size_on_drive}
    total_raw_msi: ${item.Raw_MSI}
    total_pseudocolor: ${item.Pseudocolor}
    total_pseudocolor_generation_intermediate_output: ${item.Pseudocolor_generation_intermediate_output}
    total_CJA: ${item.CJA}`;
    const txtContent = `${dataIssuetxtContent}\n\n${missingInDriveContent}\n\n${missingInExcelContent}\n\n${pieDatatxtContent}\n\n${itemDatatxtContent}`;
    const txtData = new Blob([txtContent], { type: 'text/txt;charset=utf-8;' });
    const downloadLink = document.createElement('a');
    const url = URL.createObjectURL(txtData);
    downloadLink.href = url;
    downloadLink.download = item.name + "_dataTransfer_report.txt";
    downloadLink.click();
    URL.revokeObjectURL(url);
    downloadLink.remove();
    // also call handleDownload function to download GUID List 
    handleDownload();

  }

  const renderTableRows = (item) => {
    // when selectedNavItem !== 'Patients Stat', render normally
    // when selectedNavItem === 'Patients Stat', render pie chart
    if (selectedNavItem === 'Patients Stat') {
      return (
        <DataPieChart data={pieData}/>
      )
    } else {
      // iterate over fieldNames, where each field name is a key in item. Render key and value in a table row
      return fieldNames.map((fieldName) => {
        if (fieldName === "is_match" || fieldName === "images_in_excel_without_overlap" || fieldName === "images_in_drive_without_overlap") {
          return null;
        }
        if (fieldName === "path") {
          return (
            <tr key={fieldName} >
              <td style={{ width: '30%' }} className="truncate-cell">{fieldName + " "} {copied && <Badge color="success"> Text Copied!</Badge>}</td>
              <td style={{ width: '70%' }} className="truncate-cell">
                <FaCopy onClick={handleCopyPathClick}/> {item[fieldName]} 
              </td>
            </tr>
          )
        }
        
        // Convert boolean values to strings
        const displayValue = typeof item[fieldName] === 'boolean' ? item[fieldName].toString().charAt(0).toUpperCase() + item[fieldName].toString().slice(1) : item[fieldName];
        const cls = (fieldName === "image_coll_count_in_verification_excel" || fieldName === "image_coll_count_in_drive") ? ((item["is_match"]) ? "table-success" : "table-warning") : "";
        if (fieldName === "image_coll_count_in_drive") {
          return (
            <tr key={fieldName} className={cls}>
              <td className="truncate-cell">image_coll_folder_count_in_drive</td>
              <td className="truncate-cell">{displayValue}</td>
            </tr>
          )  
        }
        return (
            <tr key={fieldName} className={cls}>
              <td className="truncate-cell">{fieldName}</td>
              <td className="truncate-cell">{displayValue}</td>
            </tr>
          )      
      }); 
    }
    
  };

  

  const handleGUIDPageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };
  const handleGUIDFirstPage = () => {
    handleGUIDPageChange(1);
  };
  
  const handleGUIDLastPage = () => {
    handleGUIDPageChange(totalPages);
  };


  const renderPagination = () => {
    const MAX_PAGES_DISPLAYED = 5;
    const paginationItems = [];

    // Add "First" page jump option
    paginationItems.push(
      <PaginationItem key="first" disabled={currentPage === 1}>
        <PaginationLink onClick={handleGUIDFirstPage}>First</PaginationLink>
      </PaginationItem>
    );

    if (totalPages <= MAX_PAGES_DISPLAYED) {
      // Render all pages
      for (let i = 1; i <= totalPages; i++) {
        paginationItems.push(
          <PaginationItem key={i} active={i === currentPage}>
            <PaginationLink onClick={() => handleGUIDPageChange(i)}>
              {i}
            </PaginationLink>
          </PaginationItem>
        );
      }
    } else {
      // Render ellipsis before and after the range of visible pages
      const rangeStart = Math.max(currentPage - Math.floor(MAX_PAGES_DISPLAYED / 2), 1);
      const rangeEnd = Math.min(rangeStart + MAX_PAGES_DISPLAYED - 1, totalPages);

      if (rangeStart > 1) {
        paginationItems.push(
          <PaginationItem key="ellipsis-start" disabled>
            <PaginationLink>...</PaginationLink>
          </PaginationItem>
        );
      }

      for (let i = rangeStart; i <= rangeEnd; i++) {
        paginationItems.push(
          <PaginationItem key={i} active={i === currentPage}>
            <PaginationLink onClick={() => handleGUIDPageChange(i)}>
              {i}
            </PaginationLink>
          </PaginationItem>
        );
      }

      if (rangeEnd < totalPages) {
        paginationItems.push(
          <PaginationItem key="ellipsis-end" disabled>
            <PaginationLink>...</PaginationLink>
          </PaginationItem>
        );
      }
    }

    // Add "Last" page jump option
    paginationItems.push(
      <PaginationItem key="last" disabled={currentPage === totalPages}>
        <PaginationLink onClick={handleGUIDLastPage}>Last</PaginationLink>
      </PaginationItem>
    );

    return paginationItems;
  };

  const handleSearchOptions = () => {
    console.log(selectedPatient);
    if (selectedPatient !== "All") {
      setSearchTerm(selectedPatient);
    } else {
      setSearchTerm("");
    }
  }

  const flattenedIssues = Object.values(dataIssues).flat();
  const combinedSet = new Set([...flattenedIssues].flatMap(set => [...set]));
  const combinedArray = Array.from(combinedSet);
  const issueCount = combinedSet.size;
  const hasIssues = issueCount !== 0;


  return (
    <div style={{ display: 'flex', height: '100vh', }}>
      <Sidebar/>
      <div style={{flex: 1, backgroundColor: '#eff5e6', maxWidth: '100%', overflowX: 'auto' }}>
        <h1 className="my-5 px-5" style={{ color: '#424a2d' }}>{item.file_type} File Info</h1> 
        <Container className="px-5">
        <Row style={{maxWidth: '100%'}}>
          <Col xs="auto">
            <Link to={`/${item.file_type}_items`} style={{ textDecoration: 'underline',textDecorationColor: '#424a2d'}}>
              <h5 outline style={{ color: '#424a2d' }}>Full {item.file_type} List</h5>
            </Link>
          </Col>
          <Col xs="auto"><span style={{ color: '#424a2d' }}>|</span></Col>
          <Col xs="auto">
            <Link to="/" style={{ textDecoration: 'underline',textDecorationColor: '#424a2d'}}>
              <h5 outline style={{ color: '#424a2d'}}>Home</h5>
            </Link>
          </Col>
          <Col xs="auto"><span style={{ color: '#424a2d' }}>|</span></Col>
          <Col xs="auto">
            <h5 outline style={{ textDecoration: 'underline', color: '#424a2d' }}
            onClick={() => handleDownloadVerificationInfo(item)}>
              <FaFileDownload />Generate Report & GUID List
            </h5>
          </Col>
          <Col xs="auto"><span style={{ color: '#424a2d' }}>|</span></Col>
          <Col xs="auto">
            <Card outline color={hasIssues ? "danger" : "success"} >
              <CardHeader className="truncate-cell" style={{ overflow: 'auto' }}>
                Immediate Issue(s)
                <Badge color={hasIssues ? "danger" : "success"}>
                  {hasIssues ? `found ${issueCount} issues` : "no issue"}
                </Badge>
              </CardHeader>
              <CardBody>
                <CardText style={{ overflow: 'auto' }}>
                  {hasIssues ? (
                    combinedArray.map((issue, index) => <li key={index}>{issue}</li>)
                  ) : (
                    "No immediate issues found"
                  )}
                </CardText>
              </CardBody>
            </Card>
          </Col>
        </Row>
        </Container>
        <br/>
          <Container>
            <Card>
              <CardHeader className="d-flex justify-content-between align-items-center" style={{ overflow: 'auto' }}>
                <div className="truncate-cell">Data Info</div>
                <Navbar color="light" expand="sm">   
                  <Nav className="ml-auto auto-resizing-button" navbar>
                    <NavItem>
                      <NavLink onClick={() => handleNavItemClick('Data Transfer Info')} className = {selectedNavItem === "Data Transfer Info"? 'active' : ""}>Data Transfer Info</NavLink>
                      {
                        dataIssues["Data Transfer Info"].size === 0? null : <Badge color="danger">!</Badge>
                      }
                    </NavItem>
                    <NavItem>
                      <NavLink onClick={() => handleNavItemClick('Collection Info')} className = {selectedNavItem === "Collection Info"? 'active' : ""}>Collection Info {/** is item.is_match is false, add a Badge next to it */}
                      {
                        dataIssues["Collection Info"].size === 0? null : <Badge color="danger">!</Badge>
                      }
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink onClick={() => handleNavItemClick('Images Categorization')} className = {selectedNavItem === "Images Categorization"? 'active' : ""}>Images Categorization</NavLink>
                      {
                        dataIssues["Images Categorization"].size === 0? null : <Badge color="danger">!</Badge>
                      }
                    </NavItem>
                    <NavItem>
                      <NavLink onClick={() => handleNavItemClick('Patients Stat')} className = {selectedNavItem === "Patients Stat"? 'active' : ""}>Patients Stat</NavLink>
                      {
                        dataIssues["Patients Stat"].size === 0? null : <Badge color="danger">!</Badge>
                      }
                    </NavItem>
                  </Nav>
                </Navbar>
              </CardHeader>
              <CardBody style={{maxWidth: '100%', overflowX: 'auto'}} >
                <Table hover className="custom-table">
                  <tbody>{renderTableRows(item)}</tbody>
                </Table>
              </CardBody>
            </Card>
            <br/>
            <Card>
              <CardHeader style={{ overflow: 'auto' }} className="d-flex justify-content-between align-items-center">
                <div className="d-flex align-items-center truncate-cell">
                  GUID List
                </div>
                <div className="d-flex justify-content-between align-items-center gap-2">
                  <input
                    type="search"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search..."
                  />
                  <IoMdOptions id="PopoverLegacy" onClick={toggleSearchForm} />
                  <UncontrolledPopover
                    placement="bottom"
                    isOpen={popoverOpen}
                    target="PopoverLegacy"
                    toggle={togglePopover}
                    trigger="legacy"
                  >
                    <PopoverHeader>Search Options</PopoverHeader>
                    <PopoverBody>
                      <form>
                        <div className="form-group">
                        <label htmlFor="patient">Patient:</label>
                            <select id="patient" className="form-control" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                              <option value="All">All</option>
                              {pieData.map((item) => (
                                <option value={item.name}>{item.name}</option>
                              ))}
                            </select>
                        </div>
                      </form>
                      <button className="btn btn-primary" onClick={handleSearchOptions}>Search</button>
                    </PopoverBody>
                  </UncontrolledPopover>
                  <Button outline className="auto-resizing-button" color="info" onClick={() => handleDownload(item)}><FaFileDownload /> Download GUID List</Button>
                </div> 
              </CardHeader>
              <CardBody style={{maxWidth: '100%', overflowX: 'auto'}} >
                <Table hover className="custom-table">
                  <thead>
                    <tr>
                      <th style={{ width: '65%' }} className="truncate-cell" onClick={() => handleGUIDColumnClick('Image Collection Folder Name')}>
                        {selectedGUIDColumn === 'Image Collection Folder Name' && (sortOrder === 'asc' ? '▲' : '▼')} Image Collection Folder Name 
                      </th>
                      <th style={{ width: '35%' }} className="truncate-cell" onClick={() => handleGUIDColumnClick('GUID')}>
                        {selectedGUIDColumn === 'GUID' && (sortOrder === 'asc' ? '▲' : '▼')} GUID 
                      </th>
                    </tr>
                  </thead>
                  <tbody>{renderGuidTableRows(item)}</tbody>       
                </Table>
              </CardBody>
              <CardFooter className="d-flex justify-content-center">
                <Pagination size="sm">{renderPagination()}</Pagination>
              </CardFooter>
            </Card> 
          </Container>
          <br></br>  
      </div>
    </div>
  ); 
}

export default ItemDetailPage;