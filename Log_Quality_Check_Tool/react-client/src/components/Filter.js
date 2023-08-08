import React, { useState } from 'react'
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import DatePicker from "react-datepicker";
import "./Filter.css"
import "react-datepicker/dist/react-datepicker.css";

const Filter = ({ setGlobalFilter, sites }) => {
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);
    const [site, setSite] = useState("");

    const applyFilter = () => {
        setGlobalFilter({ "start": startDate, "end": endDate, "site": site })
    }

    const resetChoice = () => {
        setStartDate(null)
        setEndDate(null)
        setSite("")
        setGlobalFilter({ "start": null, "end": null, "site": "" })
    }

    const sites_array = [...sites];

    return (
        <>
            <Container>
                <Row>
                    <Col>
                        <div> Start Date: </div>
                        <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
                    </Col>
                    <Col>
                        <div> End Date: </div>
                        <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} />
                    </Col>
                    <Col>
                        Choose site:
                        <Form.Select value={site} onChange={e => setSite(e.target.value)}>
                            <option value="">------</option>
                            {sites_array.map((e, key) => <option value={e} key={key}>{e}</option>)}
                        </Form.Select>
                    </Col>
                    <Col>
                        <Button onClick={applyFilter} variant="warning">Apply Filter</Button>
                    </Col>
                    <Col>
                        <Button onClick={resetChoice} variant="outline-secondary">Reset</Button>
                    </Col>
                </Row>
            </Container>

        </>
    );
}

export default Filter