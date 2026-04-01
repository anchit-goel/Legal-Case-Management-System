import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const HearingRow = ({ time, period, title, location, type }) => (
    <div className="px-8 py-5 flex items-center group hover:bg-surface-container-low transition-colors">
        <div className="w-20 text-center border-r border-outline-variant/20 mr-8">
            <p className="text-xs font-bold text-on-surface-variant uppercase">{time}</p>
            <p className="text-[10px] text-slate-400 uppercase font-medium">{period}</p>
        </div>
        <div className="flex-1">
            <h4 className="font-bold text-on-surface">{title}</h4>
            <p className="text-sm text-on-surface-variant font-medium">{location}</p>
        </div>
        <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-tighter ${
                type.includes('Trial') ? 'bg-primary-container text-on-primary-container' :
                type.includes('Evidence') ? 'bg-secondary-container text-on-secondary-container' :
                'bg-tertiary-container text-on-tertiary-container'
            }`}>
                {type}
            </span>
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState({
        active_cases: 0,
        total_cases: 0,
        total_lawyers: 0,
        total_clients: 0,
        total_hearings: 0
    });
    const [hearings, setHearings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            fetch(`${BASE_URL}/dashboard-stats`).then(res => res.json()),
            fetch(`${BASE_URL}/hearings`).then(res => res.json())
        ])
        .then(([statsData, hearingsData]) => {
            setStats(statsData || {});
            setHearings(Array.isArray(hearingsData) ? hearingsData : []);
            setLoading(false);
        })
        .catch(err => {
            console.error("Failed to load dashboard data:", err);
            setLoading(false);
        });
    }, []);

    if (loading) return <div className="p-10 flex justify-center items-center"><div className="w-8 h-8 rounded-full border-4 border-primary border-t-transparent animate-spin"></div></div>;

    return (
        <div className="pt-8 px-10 pb-12 font-body">
            <div className="mb-10 flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-extrabold text-on-surface tracking-tight leading-none mb-2 font-headline">Morning, Counselor.</h2>
                    <p className="text-on-surface-variant font-medium">Here is your live firm overview based on database records.</p>
                </div>
            </div>

            <div className="grid grid-cols-12 gap-6">
                
                <div className="col-span-12 lg:col-span-4 bg-surface-container-lowest p-6 rounded-xl shadow-sm border-l-4 border-primary">
                    <div className="flex justify-between items-start mb-4">
                        <span className="material-symbols-outlined text-primary bg-primary-container p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>groups</span>
                    </div>
                    <p className="text-sm font-bold text-on-surface-variant mb-1 uppercase tracking-widest">Total Clients</p>
                    <h3 className="text-4xl font-extrabold text-on-surface">{stats.total_clients}</h3>
                    <p className="text-[10px] mt-4 text-on-surface-variant uppercase font-bold tracking-tighter">Registered in the system</p>
                </div>

                <div className="col-span-12 lg:col-span-4 bg-surface-container-lowest p-6 rounded-xl shadow-sm border-l-4 border-secondary">
                    <div className="flex justify-between items-start mb-4">
                        <span className="material-symbols-outlined text-secondary bg-secondary-container p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>gavel</span>
                    </div>
                    <p className="text-sm font-bold text-on-surface-variant mb-1 uppercase tracking-widest">Total Lawyers</p>
                    <h3 className="text-4xl font-extrabold text-on-surface">{stats.total_lawyers}</h3>
                    <p className="text-[10px] mt-4 text-on-surface-variant uppercase font-bold tracking-tighter">Assigned as legal counsel</p>
                </div>

                <div className="col-span-12 lg:col-span-4 bg-primary text-on-primary p-6 rounded-xl shadow-lg relative overflow-hidden">
                    <div className="relative z-10">
                        <div className="flex justify-between items-start mb-4">
                            <span className="material-symbols-outlined bg-white/20 p-2 rounded-lg" style={{ fontVariationSettings: "'FILL' 1" }}>balance</span>
                        </div>
                        <p className="text-sm font-medium text-white/80 mb-1 uppercase tracking-widest font-bold">Active Cases</p>
                        <h3 className="text-4xl font-extrabold">{stats.active_cases} <span className="text-xl font-medium text-white/70">/ {stats.total_cases} Total</span></h3>
                        <p className="text-xs mt-4 text-white/80 font-medium">Currently undergoing litigation.</p>
                    </div>
                    <div className="absolute -right-10 -bottom-10 opacity-10">
                        <span className="material-symbols-outlined text-[200px]" style={{ fontVariationSettings: "'wght' 200" }}>gavel</span>
                    </div>
                </div>

                {/* Main Content Column */}
                <div className="col-span-12 lg:col-span-8 space-y-6">
                    <div className="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden">
                        <div className="px-8 py-6 flex justify-between items-center border-b border-outline-variant/5">
                            <h3 className="text-lg font-bold flex items-center gap-2 font-headline">
                                <span className="material-symbols-outlined text-primary">event_note</span>
                                Database Hearings Log
                            </h3>
                            <span className="text-xs font-bold bg-primary-container text-on-primary-container px-3 py-1 rounded-full">{stats.total_hearings} Records</span>
                        </div>
                        <div className="divide-y divide-outline-variant/10 max-h-96 overflow-y-auto">
                            {hearings.length === 0 ? (
                                <p className="p-8 text-center text-sm font-bold text-on-surface-variant">No hearings catalogued. Use the Add forms to populate actuals.</p>
                            ) : (
                                hearings.map((h, index) => {
                                    const dateObj = new Date(h.hearing_date || h[2]); // tuple or dict
                                    const notes = h.notes || h[3] || 'No notes';
                                    const cid = h.case_id || h[1];
                                    return (
                                        <HearingRow 
                                            key={h.hearing_id || h[0] || index} 
                                            time={dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                                            period=""
                                            title={`Case Assignment ID: #${cid}`} 
                                            location={notes} 
                                            type="General Hearing" 
                                        />
                                    );
                                })
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Sidebar Column */}
                <div className="col-span-12 lg:col-span-4 space-y-6">
                    <div className="bg-surface-container-lowest p-6 rounded-xl shadow-sm">
                        <h4 className="text-sm font-bold text-on-surface mb-6 font-headline flex items-center gap-2">
                            <span className="material-symbols-outlined text-secondary">add_circle</span>
                            Academic Actions
                        </h4>
                        <div className="space-y-4">
                            <Link to="/lawyers/add" className="w-full text-left py-3 px-4 bg-surface-container-high rounded-lg text-sm font-bold hover:bg-surface-container-highest transition-colors flex items-center justify-between">
                                Add Lawyer Counsel
                                <span className="material-symbols-outlined text-primary">arrow_forward</span>
                            </Link>
                            <Link to="/hearings/add" className="w-full text-left py-3 px-4 bg-surface-container-high rounded-lg text-sm font-bold hover:bg-surface-container-highest transition-colors flex items-center justify-between">
                                Assign Hearing Schedule
                                <span className="material-symbols-outlined text-primary">arrow_forward</span>
                            </Link>
                            <Link to="/clients/add" className="w-full text-left py-3 px-4 bg-surface-container-high rounded-lg text-sm font-bold hover:bg-surface-container-highest transition-colors flex items-center justify-between">
                                Formal Client Intake
                                <span className="material-symbols-outlined text-primary">arrow_forward</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
