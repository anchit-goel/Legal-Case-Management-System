import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AddHearing = () => {
    const navigate = useNavigate();
    const [cases, setCases] = useState([]);
    const [form, setForm] = useState({ case_id: '', hearing_date: '', notes: '' });
    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_BACKEND_URL || 'https://legal-case-management-system-production.up.railway.app'}/cases`)
            .then(res => res.json())
            .then(data => {
                setCases(Array.isArray(data) ? data : []);
                setFetching(false);
            })
            .catch(err => {
                console.error("Failed to fetch cases for hearing schedule:", err);
                setFetching(false);
            });
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${import.meta.env.VITE_BACKEND_URL || 'https://legal-case-management-system-production.up.railway.app'}/hearings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({...form, case_id: parseInt(form.case_id)})
            });
            if (!res.ok) throw new Error('Failed to schedule hearing');
            navigate('/');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto px-10 py-16 font-body">
            <h2 className="text-3xl font-extrabold mb-8 font-headline">Schedule Court Hearing</h2>
            <form onSubmit={handleSubmit} className="space-y-6 bg-surface-container-lowest p-8 rounded-xl shadow-sm border border-outline-variant/10">
                {error && <div className="text-red-500 font-bold mb-4">{error}</div>}
                
                <div className="flex flex-col gap-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Select Case</label>
                    {fetching ? (
                        <div className="text-sm font-bold text-slate-400">Loading cases...</div>
                    ) : (
                        <select 
                            required 
                            value={form.case_id} 
                            onChange={e => setForm({...form, case_id: e.target.value})} 
                            className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 outline-none"
                        >
                            <option value="">-- Choose an Underway Case --</option>
                            {cases.map(c => {
                                const cid = c.case_id || c[0];
                                const cnum = c.case_number || c[1];
                                const dtype = c.case_type || c[2];
                                return (
                                    <option key={cid} value={cid}>
                                        Case #{cnum} - {dtype}
                                    </option>
                                );
                            })}
                        </select>
                    )}
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Hearing Date & Time</label>
                    <input 
                        type="datetime-local"
                        required 
                        value={form.hearing_date} 
                        onChange={e => setForm({...form, hearing_date: e.target.value})} 
                        className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 outline-none" 
                    />
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Location & Notes</label>
                    <textarea 
                        required 
                        rows={3}
                        value={form.notes} 
                        onChange={e => setForm({...form, notes: e.target.value})} 
                        className="bg-surface-container-highest border-2 border-transparent border-b-primary px-4 py-3 text-sm focus:ring-0 outline-none resize-none" 
                        placeholder="Federal District Court - Room 202 - Focus: Evidentiary" 
                    />
                </div>

                <div className="pt-4 flex gap-4">
                    <button type="button" onClick={() => navigate(-1)} className="px-6 py-3 font-bold text-on-surface-variant hover:bg-surface-container-high rounded-lg transition-colors">Cancel</button>
                    <button type="submit" disabled={loading || fetching} className="flex-1 bg-primary text-on-primary font-bold py-3 rounded-lg shadow-sm hover:shadow-primary/20 transition-all">
                        {loading ? 'Submitting...' : 'Docket Notification'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AddHearing;
