import React, { useState, useContext } from 'react'
import { Button, Container, Form } from 'react-bootstrap'
import axios from 'axios';
import useAuth from "../hooks/useAuth"
import { useNavigate, useLocation, Link } from "react-router-dom";

const Login = () => {
    const { auth, setAuth } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navi = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/dashboard";


    const login = () => {
        axios.post("/login", JSON.stringify({
            "username": username,
            "password": password
        }), {
            headers: { 'Content-Type': 'application/json' },
            withCredentials: true
        }).then(res => {
            const access_token = res.data.access_token;
            const roles = res.data.roles;
            const refresh_token = res.data.refresh_token;
            setAuth({ roles, access_token })
            navi(from, { replace: true })
            localStorage.setItem('refresh_token', refresh_token);
        }).catch(error => {
            if (!error?.response) {
                console.log("No Server Response");
            } else if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
            alert('please put in the correct username and password')
            setUsername("")
            setPassword("")
        })
    }

    return <>
        <Container>
            <Form className="form">
                <h2>Log in</h2>
                <Form.Group className='mb-3'>
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        value={username}
                        onInput={e => setUsername(e.target.value)}
                    />
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        value={password}
                        type="password"
                        onInput={e => setPassword(e.target.value)}
                    />
                </Form.Group>
                <Button variant="warning" onClick={login}>Login</Button>
            </Form>
        </Container>
    </>
}

export default Login