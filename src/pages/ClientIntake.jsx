import React, { useState } from 'react';
import { BASE_URL } from '../api/config';

const ClientIntake = () => {
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleChange = e => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = e => {
        e.preventDefault();
        
        // Basic validation
        if (!form.first_name || !form.last_name || !form.email || !form.phone || !form.address) {
            setError('All fields are required');
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(form.email)) {
            setError('Please enter a valid email address');
            return;
        }
        
        // Phone validation (basic)
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(form.phone)) {
            setError('Please enter a valid phone number');
            return;
        }
        
        setLoading(true);
        setError(null);
        setSuccess(null);
        fetch(`${BASE_URL}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form),
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(data => {
                        throw new Error(data.detail || 'Failed to add client');
                    });
                }
                return res.json();
            })
            .then(() => {
                setSuccess('Client added successfully!');
                setForm({ first_name: '', last_name: '', email: '', phone: '', address: '' });
                // Clear success message after 3 seconds
                setTimeout(() => setSuccess(null), 3000);
            })
            .catch(err => setError(err.message || 'An error occurred'))
            .finally(() => setLoading(false));
    };

    return (
        <div className="max-w-6xl mx-auto px-10 py-16">
            <header className="mb-12 flex justify-between items-end">
                <div>
                    <h1 className="text-4xl font-extrabold text-on-surface tracking-tight font-headline">Client & Case Intake</h1>
                    <p className="text-on-surface-variant mt-2 text-sm max-w-lg font-body">Initiate a formal legal record. Ensure all evidence and jurisdictional details are captured with architectural precision.</p>
                </div>
                <div className="flex items-center gap-2 mb-1">
                    <span className="flex h-2 w-2 rounded-full bg-primary"></span>
                    <span className="text-xs font-bold uppercase tracking-widest text-primary font-body">Intake Phase: Information Gathering</span>
                </div>
            </header>

            <div className="grid grid-cols-12 gap-10">
                <aside className="col-span-12 lg:col-span-3 space-y-8">
                    {/* ...existing sidebar... */}
                    <div className="flex flex-col gap-6">
                        <div className="relative flex items-start gap-4">
                            <div className="z-10 flex h-8 w-8 items-center justify-center rounded-full bg-primary text-on-primary text-xs font-bold shadow-md shadow-primary/20">1</div>
                            <div className="absolute left-4 top-8 h-10 w-[2px] bg-surface-container-highest"></div>
                            <div>
                                <p className="text-sm font-bold text-on-surface">Personal Information</p>
                                <p className="text-[11px] text-on-surface-variant font-medium font-body">Identify the Subject</p>
                            </div>
                        </div>
                        {/* ...other sidebar steps... */}
                    </div>
                    <div className="p-5 bg-primary-container/30 rounded-xl border-l-4 border-primary">
                        <h4 className="text-xs font-bold text-on-primary-container uppercase tracking-widest mb-2 font-headline">Notice</h4>
                        <p className="text-xs text-on-primary-container/80 leading-relaxed font-body">Ensure all names match official government identification to avoid filing discrepancies during litigation.</p>
                    </div>
                </aside>
                <div className="col-span-12 lg:col-span-9">
                    <div className="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden p-10">
                        <form className="space-y-12" onSubmit={handleSubmit}>
                            <section>
                                <h3 className="text-xl font-bold text-on-surface font-headline mb-8 border-b border-surface-container-highest pb-4 flex items-center gap-2">
                                    <span className="material-symbols-outlined text-primary">person</span>
                                    Subject Identification
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="flex flex-col gap-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">First Name</label>
                                        <input name="first_name" value={form.first_name} onChange={handleChange} className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body" placeholder="John" type="text" required />
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Last Name</label>
                                        <input name="last_name" value={form.last_name} onChange={handleChange} className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body" placeholder="Doe" type="text" required />
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Email</label>
                                        <input name="email" value={form.email} onChange={handleChange} className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body" placeholder="j.doe@example.com" type="email" required />
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Phone</label>
                                        <input name="phone" value={form.phone} onChange={handleChange} className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body" placeholder="+1 (555) 000-0000" type="tel" required />
                                    </div>
                                    <div className="flex flex-col gap-2 md:col-span-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Address</label>
                                        <input name="address" value={form.address} onChange={handleChange} className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body" placeholder="123 Main St, City, Country" type="text" required />
                                    </div>
                                </div>
                            </section>
                            <div className="pt-8 flex items-center justify-between border-t border-surface-container-highest">
                                <button className="text-sm font-bold text-on-surface-variant hover:text-on-surface transition-colors flex items-center gap-2 font-body" type="button">
                                    <span className="material-symbols-outlined text-sm">arrow_back</span>
                                    Cancel & Discard
                                </button>
                                <div className="flex gap-4">
                                    <button className="px-10 py-3 bg-gradient-to-br from-primary to-primary-dim text-on-primary font-bold text-sm rounded-lg shadow-lg hover:shadow-primary/20 transition-all flex items-center gap-2 font-body" type="submit" disabled={loading}>
                                        {loading ? 'Submitting...' : 'Finalize Intake'}
                                        <span className="material-symbols-outlined text-sm">gavel</span>
                                    </button>
                                </div>
                            </div>
                            {error && <div className="mt-4 text-red-600 font-bold">{error}</div>}
                            {success && <div className="mt-4 text-green-600 font-bold">{success}</div>}
                        </form>
                    </div>
                </div>
            </div>
            {/* Contextual Footer Metadata */}
            <footer className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-surface-container rounded-full">
                        <span className="material-symbols-outlined text-secondary">lock</span>
                    </div>
                    <div>
                        <p className="text-xs font-bold text-on-surface">Secured Workspace</p>
                        <p className="text-[10px] text-on-surface-variant font-body">256-bit Evidence Encryption</p>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-surface-container rounded-full">
                        <span className="material-symbols-outlined text-secondary">schedule</span>
                    </div>
                    <div>
                        <p className="text-xs font-bold text-on-surface">Auto-Save Enabled</p>
                        <p className="text-[10px] text-on-surface-variant font-body">Last saved 2 minutes ago</p>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-surface-container rounded-full">
                        <span className="material-symbols-outlined text-secondary">verified</span>
                    </div>
                    <div>
                        <p className="text-xs font-bold text-on-surface">Conflict Check</p>
                        <p className="text-[10px] text-on-surface-variant font-body">Real-time database verification</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default ClientIntake;
