import React, { useState, useEffect } from 'react'
import "./Dashboard.css"
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ClinicalGraph from './ClinicalGraph';
import DeviceGraph from './DeviceGraph';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import { useNavigate, useLocation } from "react-router-dom"


const Dashboard = () => {
    const [rows, setRows] = useState([])
    const axiosPrivate = useAxiosPrivate()
    const nav = useNavigate();
    const location = useLocation();


    useEffect(() => {
        axiosPrivate.get('/getReports')
            .then(
                response => {
                    const res = response.data['row']
                    res.sort(function (a, b) {
                        const end_a = new Date(a['acquired_end_time'])
                        const end_b = new Date(b['acquired_end_time'])
                        if (end_a === end_b) {
                            return 0
                        } else if (end_a < end_b) {
                            return -1;
                        } else {
                            return 1;
                        }
                    });
                    setRows(res)
                }
            )
            .catch((err) => {
                console.log(err)
                nav("/", { state: { from: location }, replace: true });
            })
    }, [])

    console.log(rows)

    const colors = ['#e6194b', '#3cb44b', "#c99d66", '#4363d8', '#f58231', '#911eb4', '#0c3c4c',
        '#f032e6', '#f5564a', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
        '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#000000']

    if (rows.length === 0) {
        return <>Still loading...</>;
    } else {
        return (
            <>
                <Container>
                    <Row>
                        <Col>
                            <ClinicalGraph rows={rows} colors={colors} />
                        </Col>
                        <Col>
                            <DeviceGraph rows={rows} colors={colors} />
                        </Col>
                    </Row>
                </Container>
            </>
        )
    }
}

export default Dashboard