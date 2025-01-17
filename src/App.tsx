import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './Pages/main/MainPage';
import Home from './Pages/content/Home';
import Dashboard from './Pages/content/Dashboard';
import UserManage from './Pages/content/UserManage';
import DetailManage from './Pages/content/DetailManage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />}>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/user-manage" element={<UserManage />} />
          <Route path="/detail-manage" element={<DetailManage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App