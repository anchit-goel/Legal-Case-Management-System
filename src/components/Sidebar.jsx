import React from 'react';
import { Link, NavLink } from 'react-router-dom';

const Sidebar = () => (
    <aside className="h-screen w-64 fixed left-0 top-0 flex flex-col bg-slate-200 dark:bg-slate-800 py-8 px-4 gap-2 z-50">
        <div className="flex items-center gap-3 px-2 mb-6">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-lg shadow-primary/20">
                <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>account_balance</span>
            </div>
            <div>
                <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100 leading-tight">Judicial Atelier</h1>
                <p className="text-[10px] uppercase tracking-widest font-bold text-slate-500">Legal Workspace</p>
            </div>
        </div>
        <nav className="flex-1 space-y-1">
            <NavLink 
                to="/" 
                className={({ isActive }) => `relative flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'text-blue-700 dark:text-blue-400 font-bold bg-slate-300/30 before:absolute before:left-0 before:w-1 before:h-6 before:bg-blue-700 dark:before:bg-blue-400 before:rounded-r-full' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-300/50 dark:hover:bg-slate-700/50'}`}
            >
                <span className="material-symbols-outlined">dashboard</span>
                <span className="font-headline text-sm font-medium tracking-tight">Dashboard</span>
            </NavLink>
            <NavLink 
                to="/cases" 
                className={({ isActive }) => `relative flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'text-blue-700 dark:text-blue-400 font-bold bg-slate-300/30 before:absolute before:left-0 before:w-1 before:h-6 before:bg-blue-700 dark:before:bg-blue-400 before:rounded-r-full' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-300/50 dark:hover:bg-slate-700/50'}`}
            >
                <span className="material-symbols-outlined">gavel</span>
                <span className="font-headline text-sm font-medium tracking-tight">Case Management</span>
            </NavLink>
            {[
                { icon: 'group', label: 'Clients', to: '/clients' },
                { icon: 'calendar_month', label: 'Calendar', to: '/calendar' },
                { icon: 'payments', label: 'Financials', to: '/financials' },
            ].map((item) => (
                <NavLink 
                    key={item.label} 
                    to={item.to}
                    className={({ isActive }) => `relative flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${isActive ? 'text-blue-700 dark:text-blue-400 font-bold bg-slate-300/30 before:absolute before:left-0 before:w-1 before:h-6 before:bg-blue-700 dark:before:bg-blue-400 before:rounded-r-full' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-300/50 dark:hover:bg-slate-700/50'}`}
                >
                    <span className="material-symbols-outlined">{item.icon}</span>
                    <span className="font-headline text-sm font-medium tracking-tight">{item.label}</span>
                </NavLink>
            ))}
        </nav>
        <div className="mt-auto pt-6 space-y-1">
            <Link to="/create-case" className="w-full bg-primary text-on-primary py-3 rounded-xl font-bold text-sm mb-6 shadow-md hover:opacity-90 transition-all flex justify-center items-center">
                New Case
            </Link>
            <NavLink to="/settings" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-300/50 dark:hover:bg-slate-700/50 transition-colors flex items-center gap-3 px-4 py-3 rounded-lg">
                <span className="material-symbols-outlined">settings</span>
                <span className="font-headline text-sm font-medium tracking-tight">Settings</span>
            </NavLink>
            <NavLink to="/support" className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-300/50 dark:hover:bg-slate-700/50 transition-colors flex items-center gap-3 px-4 py-3 rounded-lg">
                <span className="material-symbols-outlined">help</span>
                <span className="font-headline text-sm font-medium tracking-tight">Support</span>
            </NavLink>
            <div className="flex items-center gap-3 px-4 py-4 mt-2 border-t border-slate-300/30">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex flex-col items-center justify-center text-primary font-bold text-xs font-headline">A</div>
                <div className="overflow-hidden">
                    <p className="text-xs font-bold truncate">Academic User</p>
                    <p className="text-[10px] text-slate-500">System Administrator</p>
                </div>
            </div>
        </div>
    </aside>
);

export default Sidebar;
