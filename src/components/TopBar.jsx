import React from 'react';
import { Link } from 'react-router-dom';

const TopBar = () => (
    <header className="fixed top-0 right-0 w-[calc(100%-16rem)] h-16 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl flex items-center justify-between px-8 shadow-sm">
        <div className="flex items-center gap-4 flex-1">
            <div className="relative w-full max-w-md">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">search</span>
                <input className="w-full bg-surface-container-low border-none rounded-full py-2 pl-10 pr-4 text-sm focus:ring-1 focus:ring-primary/20 outline-none" placeholder="Search cases, documents, or clients..." type="text" />
            </div>
        </div>
        <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
                <button className="p-2 text-slate-500 hover:text-primary transition-colors relative">
                    <span className="material-symbols-outlined">notifications</span>
                    <span className="absolute top-2 right-2 w-2 h-2 bg-error rounded-full"></span>
                </button>
                <button className="p-2 text-slate-500 hover:text-primary transition-colors">
                    <span className="material-symbols-outlined">history</span>
                </button>
            </div>
            <div className="h-8 w-[1px] bg-outline-variant/30"></div>
            <div className="flex items-center gap-3">
                <button className="px-4 py-2 text-sm font-semibold text-primary hover:bg-primary-container rounded-lg transition-colors">Export</button>
                <Link to="/intake" className="px-5 py-2 text-sm font-bold bg-primary text-on-primary rounded-lg shadow-sm scale-95 active:scale-100 transition-transform flex items-center justify-center">Add Entry</Link>
            </div>
        </div>
    </header>
);

export default TopBar;
