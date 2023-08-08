import React from 'react'
import Navbar from 'react-bootstrap/Navbar';
import axios from 'axios';
import useAuth from '../hooks/useAuth';

const Logout = () => {
    const { auth, setAuth } = useAuth();

    const logMeOut = () => {
        axios.post("/logout")
            .then((response) => {
                setAuth({})
                localStorage.removeItem('refresh_token');
            }).catch((error) => {
                if (error.response) {
                    console.log(error.response)
                    console.log(error.response.status)
                    console.log(error.response.headers)
                }
            })
    }

    return (
        <Navbar.Text onClick={logMeOut} className="login">Log out</Navbar.Text>
    )
}

export default Logout