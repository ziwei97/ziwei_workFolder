import './App.css';
import React, { Component } from "react";
import {Route, Routes} from "react-router-dom";
import ItemDetailPage from './components/ItemDetailPage';
import Home from './components/Home';
import {BurnList, DFUList} from './components/ItemList'
import ExampleThing from './components/ServerBarChart';

class App extends Component {
  render() {
    return (
    <Routes>
      <Route exact path="/" element={<Home />} />
      <Route exact path="/DFU_items" element={<DFUList />} />
      <Route exact path="/Burn_items" element={<BurnList />} />
      <Route exact path="/item/:id" element={<ItemDetailPage />} />
      <Route exact path="/test" element={<ExampleThing />} />

    </Routes>
  )}
}

export default App;
