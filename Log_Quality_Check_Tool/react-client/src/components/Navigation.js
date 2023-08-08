import React from 'react'
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Logout from './Logout';
import { Link } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

const Navigation = () => {
  const { auth, setAuth } = useAuth();

  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Link to="/dashboard" className='title'>Data Pipeline Web Portal</Link>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Nav>
            <Link to="/details" className='title details'>details</Link>
          </Nav>
          {auth.access_token ? <Logout /> : null}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Navigation