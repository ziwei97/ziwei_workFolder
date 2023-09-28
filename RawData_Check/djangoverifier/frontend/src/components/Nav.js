import React from 'react';
import { Nav, NavItem, NavbarBrand, NavLink } from 'reactstrap';
import {FaFire, FaHome} from "react-icons/fa";
import {GiBarefoot} from "react-icons/gi";
import { Link } from 'react-router-dom';
import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarFooter,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem,
} from 'cdbreact';

import '../App.css';

export function DataCheckNav() {
    return (
      <Nav vertical>
      <NavbarBrand>
        <NavLink href="/">
          Data Checker
        </NavLink>
      </NavbarBrand>
      <NavItem>
        <NavLink tag={Link} to="/" >
          Home
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink tag={Link} to="/DFU_items">
          DFU Verified Files
        </NavLink>
      </NavItem>
      <NavItem>
        <NavLink tag={Link} to="/Burn_items">
          Burn Verified Files
        </NavLink>
      </NavItem>
    </Nav>
  );
};

export const Sidebar = () => {
  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'scroll initial' }}>
      <CDBSidebar textColor="#fff" backgroundColor="#424a2d">
        <CDBSidebarHeader prefix={<i className="fa fa-bars fa-large"></i>}>
          <a href="/" className="text-decoration-none" style={{ color: 'inherit' }}>
            Data Checker
          </a>
        </CDBSidebarHeader>

        <CDBSidebarContent className="sidebar-content">
          <CDBSidebarMenu>
            <NavLink tag={Link} to="/" activeClassName="activeClicked">
              <CDBSidebarMenuItem><FaHome style={{ marginRight: '16px' }}/>Home</CDBSidebarMenuItem>
            </NavLink>
            <NavLink tag={Link} to="/DFU_items" activeClassName="activeClicked">
              <CDBSidebarMenuItem><GiBarefoot style={{ marginRight: '16px' }}/>DFU Files</CDBSidebarMenuItem>
            </NavLink>
            <NavLink tag={Link} to="/Burn_items" activeClassName="activeClicked">
              <CDBSidebarMenuItem><FaFire style={{ marginRight: '16px' }}/>Burn Files</CDBSidebarMenuItem>
            </NavLink>
          </CDBSidebarMenu>
        </CDBSidebarContent>

        <CDBSidebarFooter style={{ textAlign: 'center', overflow: 'hidden' }}>
          <div
            className="sidebar-btn-wrapper"
            style={{
              padding: '20px 5px',
            }}
          >
            SpectralMD
          </div>
        </CDBSidebarFooter>
      </CDBSidebar>
    </div>
  );
};



