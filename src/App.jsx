import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import Dashboard from './pages/Dashboard';
import CaseManagement from './pages/CaseManagement';
import CaseDetails from './pages/CaseDetails';
import ClientIntake from './pages/ClientIntake';
import CreateCase from './pages/CreateCase';
import Clients from './pages/Clients';
import AddLawyer from './pages/AddLawyer';
import AddHearing from './pages/AddHearing';

const App = () => {
    return (
        <Router>
            <div className="min-h-screen bg-surface selection:bg-primary-container selection:text-on-primary-container">
                <Sidebar />
                <main className="ml-64 min-h-screen">
                    <TopBar />
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/cases" element={<CaseManagement />} />
                        <Route path="/cases/:id" element={<CaseDetails />} />
                        <Route path="/intake" element={<ClientIntake />} />
                        <Route path="/create-case" element={<CreateCase />} />
                        <Route path="/clients" element={<Clients />} />
                        <Route path="/clients/add" element={<ClientIntake />} />
                        <Route path="/lawyers/add" element={<AddLawyer />} />
                        <Route path="/hearings/add" element={<AddHearing />} />
                        <Route path="/calendar" element={<div className="p-10">Calendar Page Coming Soon</div>} />
                        <Route path="/financials" element={<div className="p-10">Financials Page Coming Soon</div>} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

export default App;
