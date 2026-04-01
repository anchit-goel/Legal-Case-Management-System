import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AddLawyer = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState({ name: '', specialization: '' });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const base = import.meta.env.VITE_BACKEND_URL || '/api';
            const res = await fetch(`${base}/lawyers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(form)
            });
            if (!res.ok) {
                const body = await res.json().catch(() => ({}));
            throw new Error(`Failed to add lawyer (${res.status}): ${body.detail || 'Unknown error'}`);
            }
            navigate('/');
        }  catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto px-10 py-16 font-body">
            <h2 className="text-3xl font-extrabold mb-8 font-headline">Add Legal Counsel</h2>
            <form onSubmit={handleSubmit} className="space-y-6 bg-surface-container-lowest p-8 rounded-xl shadow-sm border border-outline-variant/10">
                {error && <div className="text-red-500 font-bold mb-4">{error}</div>}
                
                <div className="flex flex-col gap-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Full Name (Esq.)</label>
                    <input 
                        required 
                        value={form.name} 
                        onChange={e => setForm({...form, name: e.target.value})} 
                        className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 outline-none" 
                        placeholder="Atticus Finch" 
                    />
                </div>

                <div className="flex flex-col gap-2">
                    <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Legal Specialization</label>
                    <input 
                        required 
                        value={form.specialization} 
                        onChange={e => setForm({...form, specialization: e.target.value})} 
                        className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 outline-none" 
                        placeholder="Corporate Defense" 
                    />
                </div>

                <div className="pt-4 flex gap-4">
                    <button type="button" onClick={() => navigate(-1)} className="px-6 py-3 font-bold text-on-surface-variant hover:bg-surface-container-high rounded-lg transition-colors">Cancel</button>
                    <button type="submit" disabled={loading} className="flex-1 bg-primary text-on-primary font-bold py-3 rounded-lg shadow-sm hover:shadow-primary/20 transition-all">
                        {loading ? 'Filing...' : 'Authorize Counsel'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AddLawyer;
