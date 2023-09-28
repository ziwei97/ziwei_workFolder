import React, { useState, useEffect } from 'react';
import { Button,
  Card, CardBody, CardHeader, CardFooter, CardTitle,
  Table, Container, 
  Pagination, PaginationItem, PaginationLink, Alert, UncontrolledAlert,
  PopoverHeader, PopoverBody, UncontrolledPopover,
  } from 'reactstrap';
import PropTypes from 'prop-types';
import axios from 'axios';
import '../App.css';
import { useNavigate, Link } from 'react-router-dom';
import { FaRedo, FaSpinner, FaHome } from 'react-icons/fa';
import { AiOutlineCloudServer } from "react-icons/ai";
import { GiCancel } from "react-icons/gi";
import { Sidebar } from './Nav';
import { IoMdOptions } from "react-icons/io";
import ExampleThing from './ServerBarChart';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";



export function ItemList({ apiEndpoint, pageTitle }) {
  const navigate = useNavigate();
  
  const [driverInfoList, setDriverInfoList] = useState([]);
  const [selectAll, setSelectAll] = useState(false);
  const [selected, setSelected] = useState([]); // { 2: true, 3: false }
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 10;
  const [selectedColumn, setSelectedColumn] = useState('dataArrivalDate');
  const [sortOrder, setSortOrder] = useState(selectedColumn === 'dataArrivalDate' ? 'desc' : 'asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredItems, setFilteredItems] = useState(driverInfoList);
  const [loadingRows, setLoadingRows] = useState([]);
  const [barChartData, setBarChartData] = useState([]);
  

  // The following are for alert messages
  const [infoVerificationAlert, setInfoVerificationAlert] = useState([]);
  const [refreshAlert, setRefreshAlert] = useState(false);
  const [refreshFailedAlert, setRefreshFailedAlert] = useState(false);

  // The following are for Serach Options popover
  const [showSearchForm, setShowSearchForm] = useState(false);
  const [popoverOpen, setPopoverOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState('All');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [searchOptionItems, setSearchOptionItems] = useState([]);
  const [searchOptionActived, setSearchOptionActived] = useState(false);
  const [resultString, setResultString] = useState('');


  useEffect(() => {
    let timeoutId;
  
    if (refreshAlert) {
      timeoutId = setTimeout(() => {
        setRefreshAlert(false);
      }, 2000);
      console.log('Data refresh triggered and succeeded');
    }
    
    return () => {
      clearTimeout(timeoutId);
    };
  }, [refreshAlert]);
  

  const toggleSearchForm = () => {
    setShowSearchForm(!showSearchForm);
    console.log("search option clicked")
  };

  const togglePopover = () => {
    setPopoverOpen(!popoverOpen);
    console.log("Search option popover state changed")
  }

  const sortItems = (items, column, order) => {
    const sortedItems = items.slice().sort((a, b) => {
      if (column === 'site') {
        return a[0].split('/')[2].localeCompare(b[0].split('/')[2]);
      } else if (column === 'dataArrivalDate') {
        return new Date(a[1]) - new Date(b[1]);
      } else if (column === 'path') {
        return a[0].localeCompare(b[0]);
      }
      return 0;
    });
    if (order === 'desc') {
      sortedItems.reverse();
    }
    console.log(`Sort by ${column} in ${order} order}`)
    return sortedItems;
  };

  const getFilteredItems = (items, searchTerm) => {
    console.log(`Filter by ${searchTerm}`);
    return items.filter((item) => {
      const rowData = item[0] + item[1]; // Adjust as per your column data
      return rowData.toLowerCase().includes(searchTerm.toLowerCase());
    });
  };

  const sortAndFilter = (items, column, order, searchTerm) => {
    const sortedItems = sortItems(items, column, order);
    const filteredItems = getFilteredItems(sortedItems, searchTerm);
    setFilteredItems(filteredItems);
    const newTotalPages = calculateTotalPages(filteredItems, itemsPerPage);
    setTotalPages(newTotalPages);
    setCurrentPage(1);
    return filteredItems;
  };

  useEffect(() => {
    if (driverInfoList.length === 0) {
      axios.get(`http://localhost:8000/api/cached-items/${apiEndpoint}`).then((res) => {
      const data = res.data.subfolders;
      const site_stats = res.data.site_stats;
      const site_stats_dict = Object.keys(site_stats).map((key) => {
        return {name: key, file_count: site_stats[key]};
      });
      setBarChartData(site_stats_dict);
      setDriverInfoList(data);
      sortAndFilter(data, selectedColumn, sortOrder, searchTerm);
      console.log("ItemList data loaded")
     }).catch((err) => console.log(err));
    } else if (searchOptionActived === false) {
      sortAndFilter(driverInfoList, selectedColumn, sortOrder, searchTerm);
    } else {
      sortAndFilter(searchOptionItems, selectedColumn, sortOrder, searchTerm);
    }
  }, [searchTerm, sortOrder, apiEndpoint]);

  useEffect(() => {
    if (searchOptionItems.length === 0) {
      setSearchOptionActived(false);
    } else {
      setSearchOptionActived(true);
    }
  }, [searchOptionItems]);


  const handleDelete = () => {
    const confirmation = window.confirm('Are you sure you want to re-verify the item(s)?');
    if (!confirmation) return;
    try {
      // loop through selected items and delete them
      for (let i = 0; i < selected.length; i++) {
        axios.get(`http://localhost:8000/api/data_delete/${selected[i][0]}/`);
        // axios.delete(`http://localhost:8000/api/guid_lists/${selected[i][1]}/`);
      }
      
      setSelected([]);
      if (selectAll) setSelectAll(false);
      // axios.delete(`http://localhost:8000/api/data_file_infos/${item.id}/`).then((res) => refreshList());
      setRefreshAlert(true);
      // alert('Re-verification complete!'); // lmao can we make this good
      console.log('Re-fresh useEffect complete!');
    } catch (error) {
      // Handle error
      setRefreshFailedAlert(true);
      console.error(error);
      // Display an error message to the user or perform any necessary actions
    }
  };

  const handleInfoClick = (itemPath, date) => {
    setLoadingRows([...loadingRows, itemPath]);
    // First do a bunch of maneuvering to get the item in the database 
    // And then we will be able to get the id of the item in the database
    // Then we can use the id to navigate to the item detail page
    axios.get(`http://localhost:8000/api/handle-info-click/${itemPath}/${date}`)
    .then(response => {
      // Process the item data or update the state as needed
      const id = response.data['id'];
      navigate(`/item/${id}`, { target: '_blank', rel: 'noopener noreferrer' });
    })
    .catch(error => {
      setInfoVerificationAlert([...infoVerificationAlert, itemPath]);
      console.error(error);
    })
    .finally(() => {
      setLoadingRows(loadingRows.filter((row) => row !== itemPath));
      console.log('Info verification complete!');
    });
  };

  const handleCheckboxChange = (path, date) => {
    if (selected.some(item => item[0] === path && item[1] === date)) {
      setSelected(selected.filter(item => item[0] !== path || item[1] !== date));
    } else {
      setSelected([...selected, [path, date]]);
    }
    console.log(`Selected: ${path} ${date}`)
  };   


  const handleSelectAll = () => {
    const newSelected = [];
    if (selectAll) {
      setSelectAll(false);
      setSelected(newSelected);
      console.log("unselect all")
    } else {
      filteredItems.forEach((item) => {
        newSelected.push([item[0], item[1]]);
      });
      setSelectAll(true);
      setSelected(newSelected);
      console.log("select all")
    }
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    console.log(`Currently viewing ${pageNumber} on itmeList page`);
  };
  const handleFirstPage = () => {
    handlePageChange(1);
    console.log(`Currently viewing first page on itmeList page`)
  };
  
  const handleLastPage = () => {
    handlePageChange(totalPages);
    console.log(`Currently viewing last page on itmeList page`)
  };

  const renderPagination = () => {
    const MAX_PAGES_DISPLAYED = 5;
    const paginationItems = [];

    // Add "First" page jump option
    paginationItems.push(
      <PaginationItem key="first" disabled={currentPage === 1}>
        <PaginationLink onClick={handleFirstPage}>First</PaginationLink>
      </PaginationItem>
    );

    if (totalPages <= MAX_PAGES_DISPLAYED) {
      // Render all pages
      for (let i = 1; i <= totalPages; i++) {
        paginationItems.push(
          <PaginationItem key={i} active={i === currentPage}>
            <PaginationLink onClick={() => handlePageChange(i)}>
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
            <PaginationLink onClick={() => handlePageChange(i)}>
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
        <PaginationLink onClick={handleLastPage}>Last</PaginationLink>
      </PaginationItem>
    );

    return paginationItems;
  };

  const handleColumnClick = (column) => {
    if (column === selectedColumn) {
      // If the same column is clicked, toggle the sort order
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      // If a different column is clicked, set it as the selected column and default to ascending order
      setSelectedColumn(column);
      setSortOrder('asc');
    }
    console.log(`Currently sorting by ${column} in ${sortOrder} order`)
  };

  const calculateTotalPages = (items, itemsPerPage) => {
    return Math.ceil(items.length / itemsPerPage);
  };

  const renderBarChart = (data) => {
    console.log("rendering bar chart");
    if (data.length === 0) {
      return (
        <div className="d-flex justify-content-center align-items-center" >
          <FaSpinner className="spinner" />
        </div>
      );
    }
    return (
      <ExampleThing data={data}/>
    );
  };

  const renderItems = () => {
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = filteredItems.slice(indexOfFirstItem, indexOfLastItem);
    console.log(`Rendering data from ${apiEndpoint}`)
    return (
      <Table bordered className="custom-table">
        <thead>
          <tr>
            <th style={{ width: '2%' }} className="checkbox-cell" >
            <input 
              type="checkbox"
              checked={selectAll}
              onChange={handleSelectAll}
            />
            </th>
            <th style={{ width: '5%' }} className="truncate-cell" onClick={() => handleColumnClick('site')}>  
              {selectedColumn === 'site' && (
                <span>{sortOrder === 'asc' ? ' ▼' : ' ▲'}</span>
              )}
              Site
            </th>
            <th style={{ width: '10%' }} className="truncate-cell" onClick={() => handleColumnClick('dataArrivalDate')}>
              {selectedColumn === 'dataArrivalDate' && (
                <span>{sortOrder === 'asc' ? ' ▼' : ' ▲'}</span>
              )}
              Data Arrival Date
            </th>
            <th style={{ width: '30%' }} className="truncate-cell" onClick={() => handleColumnClick('path')}>
              {selectedColumn === 'path' && (
                <span>{sortOrder === 'asc' ? ' ▼' : ' ▲'}</span>
              )}
              Remote File Path
            </th>
            <th style={{ width: '5%' }} className="truncate-cell"></th>
          </tr>
        </thead>
        <tbody>
          {currentItems.map((item) => (
            <tr key={item.id}>
              <td className="checkbox-cell">
                <input 
                  type="checkbox"
                  checked={selected.some(i => i[0] === item[0] && i[1] === item[1])}
                  onChange={() => handleCheckboxChange(item[0], item[1])}
                />
              </td>
              <td className="truncate-cell" >{item[0].split('/')[2]}</td>
              {/*turn 060823 to 06/08/23*/}
              <td className="truncate-cell">{item[1]}</td>
              <td className="truncate-cell">{item[0]}</td>
              {/* <td>{item.image_coll_count_in_drive}</td>
              <td>{item.images_count}</td> */}
              <td className="table-button-cell truncate-cell">
              <div className="d-flex justify-content-center">
                <Button className="btn btn-secondary mr-2r auto-resizing-button" style={{color:"#065c06", background:"#c7f0c7"}} key={`${item[0]}_${item[1]}`} onClick={() => handleInfoClick(item[0], item[1])}>
                  {loadingRows.includes(item[0]) ? (
                    <FaSpinner className="spinner" />
                  ) : (
                    'Info'
                  )}
                </Button>
              </div>        
              </td>
            </tr>
          ))}
        </tbody>
      </Table>  
    );
  };

  const generateResultString = () => {
    if (selectedLocation === 'All' && startDate === null && endDate === null) {
      return 'Showing all data';
    } else {
      const start = startDate === null? "the beginning" : startDate.toISOString().split('T')[0];
      const end = endDate === null? "today" : endDate.toISOString().split('T')[0];
      return `Showing ${selectedLocation.toLocaleLowerCase() + ' site'} data from ${start} to ${end}`;
    }
  }
  const handleSearchOptions = () => {  
    const start = startDate === null? (new Date('1970-01-01')) : startDate;
    const end = endDate === null? (new Date()) : endDate;
    start.setHours(0,0,0,0);
    end.setHours(0,0,0,0);
    
    const filteredData = driverInfoList.filter((item) => {
      if (selectedLocation === 'All') return true;
      return item[0].split('/')[2] === selectedLocation;
    }
    ).filter((item) => {
      const date = item[1].split(' ')[0];
      const convert = new Date(date);
      convert.setHours(0,0,0,0);
      return convert >= start && convert <= end;
    }
    );
    const str = generateResultString();
    setResultString(str);
    setSearchOptionItems(filteredData);
    setSearchOptionActived(true);
    // Lastly apply the searchTerm
    sortAndFilter(filteredData, selectedColumn, sortOrder, searchTerm);
  }

  const clearAllSearchOption = () => {
    setSearchOptionItems([]);
    setSearchOptionActived(false);
    setSelectedLocation('All');
    setStartDate(null);
    setEndDate(null);
    sortAndFilter(driverInfoList, selectedColumn, sortOrder, searchTerm);
  }

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'scroll initial' }}>
        {/* <Container fluid style={{ backgroundColor: '#FBFAF0', minHeight: '100vh' }}> */}
        <Sidebar/>
        <div style={{ flex: 1, backgroundColor: '#eff5e6', maxWidth: '100%', overflowX: 'auto' }}>
          <h1 className="my-5 px-5" style={{ color: '#424a2d' }}>{pageTitle}</h1>
          <Link to="/" style={{ textDecoration: 'none' }}>
            <h4 outline className="px-5" style={{color: '#424a2d'}}><FaHome style={{ marginRight: '1%' }}/>Return to Home Page</h4>
          </Link>
          <Container>
            <Card>
                {renderBarChart(barChartData)}
            </Card>
          </Container>  
          <br/>  
          <Container>
            <div className="d-flex justify-content-center align-items-center">
              <Card>
                {infoVerificationAlert.length > 0 && (
                  // map infoVerificationAlert array 
                  infoVerificationAlert.map((item) => (
                    <UncontrolledAlert color="danger">
                      <h5 className="alert-heading">
                        Failed: {item}
                      </h5>
                      Please check the data format in local server. 
                    </UncontrolledAlert>
                  ))
                )}
                {refreshAlert && (
                  <Alert color="success">
                    Data clear succeed.
                  </Alert>
                )}
                {refreshFailedAlert && (
                  <UncontrolledAlert color="success">
                    Data clear failed. Try checking network connection or other troubleshooting method.
                  </UncontrolledAlert>
                )}
                <CardHeader className="d-flex justify-content-between align-items-center" style={{ overflow: 'auto' }}>
                  <div className="truncate-cell" >
                    <span>Data on {`192.168.110.252/${apiEndpoint}`}</span>  
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
                            <label htmlFor="location">Location:</label>
                            <select id="location" className="form-control" value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
                              <option value="All">All</option>
                              {barChartData.map((item) => (
                                <option value={item.name}>{item.name}</option>
                              ))}
                            </select>
                            <br/>
                            <label htmlFor="date">Date Range:</label>
                            <br/>
                            from: <DatePicker 
                              isClearable
                              id="date" 
                              filterDate={d => {
                                return new Date() > d;
                              }}
                              placeholderText="Select Start Date"
                              dateFormat="yyyy-MM-dd"
                              selected={startDate}
                              selectsStart
                              startDate={startDate}
                              endDate={endDate}
                              onChange={date => setStartDate(date)}
                            />
                            <br/>
                            to: <DatePicker
                              isClearable
                              id="date" 
                              filterDate={d => {
                                return new Date() > d;
                              }}
                              placeholderText="Select End Date"
                              dateFormat="yyyy-MM-dd"
                              selected={endDate}
                              selectsEnd
                              startDate={startDate}
                              endDate={endDate} // May change later according to actual data arrival range
                              minDate={startDate}
                              onChange={date => setEndDate(date)}
                            />
                            <br/>
                          </div>
                        </form>
                        <Button className="btn btn-info" onClick={handleSearchOptions}>Search</Button>
                      </PopoverBody>
                    </UncontrolledPopover>
                    <Button color="primary" className="auto-resizing-button" disabled={selected.length === 0}>
                      <AiOutlineCloudServer /> Upload to Cloud
                    </Button>
                    <Button color="warning" className="auto-resizing-button" onClick={handleDelete} disabled={selected.length === 0}>
                      <FaRedo /> Clear Data
                    </Button>
                  </div>         
                </CardHeader>
                <CardBody outline className="truncate-cell" style={{ maxHeight: '100%', overflow: 'auto'}}>     
                  <CardTitle tag="h6">
                    {searchOptionActived ? (
                      <>
                        {resultString} {resultString === "Showing all data"? null : <GiCancel onClick={clearAllSearchOption}/>}
                      </>
                    ) : "Showing all data"}
                  </CardTitle>
                  {renderItems()}
                </CardBody>
                <CardFooter className="d-flex justify-content-center">
                <Pagination size="sm">{renderPagination()}</Pagination>
                </CardFooter>
              </Card>
            </div>
          </Container>
          <br/>
        </div>  
    </div>
  );
}

ItemList.propTypes = {
    apiEndpoint: PropTypes.string.isRequired,
    pageTitle: PropTypes.string.isRequired, 
    navigate: PropTypes.func.isRequired,
};

export function DFUList() {
  return <ItemList apiEndpoint="DFU" pageTitle="DFU Data Files" />;
}

export function BurnList() {
  return <ItemList apiEndpoint="EPOC" pageTitle="Burn Data Files" />;
}
