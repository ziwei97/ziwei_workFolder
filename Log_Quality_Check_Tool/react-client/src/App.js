import './App.css';
import react, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Table from './components/Table';
import { BrowserRouter, Routes, Route, } from "react-router-dom";
import Dashboard from './components/Dashboard';
import Navigation from './components/Navigation';
import Login from './components/Login';
import useAuth from "./hooks/useAuth"
import Layout from './components/Layout';
import Missing from './components/Missing';
import RequireAuth from './components/RequireAuth';
import PersistLogin from './components/PersistLogin';

function App() {

  return (
    <>
      <Navigation />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/" element={<Login />}></Route>

          <Route element={<PersistLogin />}>
            <Route element={<RequireAuth />}>
              <Route path="dashboard" element={<Dashboard />}></Route>
              <Route path="details" element={<Table />}></Route>
            </Route>
          </Route>

          <Route path="*" element={<Missing />}></Route>

        </Route>
      </Routes>
    </>
  )
}

export default App;
