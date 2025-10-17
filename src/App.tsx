import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Tracker from './pages/Tracker';
import DashboardLayout from "./pages/DashboardLayout";


import './styles/tailwind.css';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route element={<DashboardLayout />}>
        <Route path="/tracker" element={<Tracker />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
