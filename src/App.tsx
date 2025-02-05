import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './Pages/main/MainPage';
import Home from './Pages/content/Home';
import Dashboard from './Pages/content/Dashboard';
import UserManage from './Pages/content/UserManage';
import DetailManage from './Pages/content/DetailManage';
import EmptyPage from './Pages/main/EmptyPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainPage />}>
          <Route path="/" element={<Home />} />
          <Route path="/user-manage" element={<UserManage />} />
          <Route path="/detail-manage" element={<DetailManage />} />
        </Route>
        <Route element={<EmptyPage />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </Router >
  );
}

export default App