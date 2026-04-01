import React, { useState, useEffect } from 'react';
import { BASE_URL } from '../api/config';
import { useNavigate } from 'react-router-dom';

const CreateCase = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        case_number: '',
        case_type: '',
        client_id: '',
        lawyer_id: '',
        filing_date: '',
        description: '',
    });
    const [clients, setClients] = useState([]);
    const [lawyers, setLawyers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [loadingData, setLoadingData] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    // Load clients and lawyers on mount
    useEffect(() => {
        setLoadingData(true);
        Promise.all([
            fetch(`${BASE_URL}/clients`).then(r => r.ok ? r.json() : []),
            fetch(`${BASE_URL}/lawyers`).then(r => r.ok ? r.json() : [])
        ])
            .then(([clientsData, lawyersData]) => {
                setClients(clientsData || []);
                setLawyers(lawyersData || []);
            })
            .catch(err => setError('Failed to load clients or lawyers'))
            .finally(() => setLoadingData(false));
    }, []);

    const handleChange = e => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = e => {
        e.preventDefault();
        
        // Validation
        if (!form.case_number || !form.case_type || !form.client_id || !form.lawyer_id || !form.filing_date || !form.description) {
            setError('All fields are required');
            return;
        }

        setLoading(true);
        setError(null);
        setSuccess(null);

        fetch(`${BASE_URL}/cases`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                case_number: form.case_number,
                case_type: form.case_type,
                client_id: parseInt(form.client_id),
                lawyer_id: parseInt(form.lawyer_id),
                filing_date: form.filing_date,
                description: form.description,
            }),
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(data => {
                        throw new Error(data.detail || 'Failed to create case');
                    });
                }
                return res.json();
            })
            .then(() => {
                setSuccess('Case created successfully!');
                setForm({
                    case_number: '',
                    case_type: '',
                    client_id: '',
                    lawyer_id: '',
                    filing_date: '',
                    description: '',
                });
                // Redirect to cases page after 1.5 seconds
                setTimeout(() => navigate('/cases'), 1500);
            })
            .catch(err => setError(err.message || 'An error occurred'))
            .finally(() => setLoading(false));
    };

    if (loadingData) {
        return (
            <div className="p-10 max-w-4xl mx-auto">
                <div className="text-center text-lg">Loading form data...</div>
            </div>
        );
    }

    if (clients.length === 0 || lawyers.length === 0) {
        return (
            <div className="p-10 max-w-4xl mx-auto">
                <div className="bg-yellow-100 text-yellow-800 p-6 rounded-lg">
                    <p className="font-bold">Unable to create case</p>
                    <p className="text-sm mt-2">
                        {clients.length === 0 ? 'No clients available. ' : ''}
                        {lawyers.length === 0 ? 'No lawyers available. ' : ''}
                        Please add these first.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto px-10 py-16">
            <header className="mb-12">
                <h1 className="text-4xl font-extrabold text-on-surface tracking-tight font-headline mb-2">Create New Case</h1>
                <p className="text-on-surface-variant text-sm font-body">Establish a new legal matter with comprehensive case information.</p>
            </header>

            <div className="bg-surface-container-lowest rounded-xl shadow-sm p-10">
                <form className="space-y-8" onSubmit={handleSubmit}>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Case Number */}
                        <div className="flex flex-col gap-2">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Case Number</label>
                            <input
                                type="text"
                                name="case_number"
                                value={form.case_number}
                                onChange={handleChange}
                                placeholder="e.g., 2024-001"
                                className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body"
                                required
                            />
                        </div>

                        {/* Case Type */}
                        <div className="flex flex-col gap-2">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Case Type</label>
                            <input
                                type="text"
                                name="case_type"
                                value={form.case_type}
                                onChange={handleChange}
                                placeholder="e.g., Corporate Law"
                                className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body"
                                required
                            />
                        </div>

                        {/* Client Dropdown */}
                        <div className="flex flex-col gap-2">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Client</label>
                            <select
                                name="client_id"
                                value={form.client_id}
                                onChange={handleChange}
                                className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body"
                                required
                            >
                                <option value="">Select a Client</option>
                                {clients.map(client => (
                                    <option key={client.client_id} value={client.client_id}>
                                        {client.first_name} {client.last_name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Lawyer Dropdown */}
                        <div className="flex flex-col gap-2">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Assigned Lawyer</label>
                            <select
                                name="lawyer_id"
                                value={form.lawyer_id}
                                onChange={handleChange}
                                className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body"
                                required
                            >
                                <option value="">Select a Lawyer</option>
                                {lawyers.map(lawyer => (
                                    <option key={lawyer.lawyer_id} value={lawyer.lawyer_id}>
                                        {lawyer.name} ({lawyer.specialization})
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Filing Date */}
                        <div className="flex flex-col gap-2">
                            <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Filing Date</label>
                            <input
                                type="date"
                                name="filing_date"
                                value={form.filing_date}
                                onChange={handleChange}
                                className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body"
                                required
                            />
                        </div>
                    </div>

                    {/* Description */}
                    <div className="flex flex-col gap-2">
                        <label className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant font-body">Case Description</label>
                        <textarea
                            name="description"
                            value={form.description}
                            onChange={handleChange}
                            placeholder="Provide a comprehensive overview of the case..."
                            className="bg-surface-container-highest border-b-2 border-primary border-t-0 border-l-0 border-r-0 px-4 py-3 text-sm focus:ring-0 focus:border-primary-dim transition-all outline-none font-body min-h-[120px]"
                            required
                        />
                    </div>

                    {/* Messages */}
                    {error && <div className="p-4 bg-red-100 text-red-700 rounded-lg text-sm font-bold">{error}</div>}
                    {success && <div className="p-4 bg-green-100 text-green-700 rounded-lg text-sm font-bold">{success}</div>}

                    {/* Buttons */}
                    <div className="pt-8 flex items-center justify-between border-t border-surface-container-highest">
                        <button
                            type="button"
                            onClick={() => navigate('/cases')}
                            className="text-sm font-bold text-on-surface-variant hover:text-on-surface transition-colors flex items-center gap-2 font-body"
                        >
                            <span className="material-symbols-outlined text-sm">arrow_back</span>
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-10 py-3 bg-gradient-to-br from-primary to-primary-dim text-on-primary font-bold text-sm rounded-lg shadow-lg hover:shadow-primary/20 transition-all flex items-center gap-2 font-body disabled:opacity-50"
                        >
                            {loading ? 'Creating...' : 'Create Case'}
                            <span className="material-symbols-outlined text-sm">gavel</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateCase;
