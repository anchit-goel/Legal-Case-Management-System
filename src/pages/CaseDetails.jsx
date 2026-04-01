import React, { useState, useEffect } from 'react';
import { BASE_URL } from '../api/config';
import { useParams, Link } from 'react-router-dom';

const CaseDetails = () => {
    const { id } = useParams();
    const [caseData, setCaseData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!id) {
            setError("No case ID provided");
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);
        fetch(`${BASE_URL}/cases/${id}`)
            .then(res => {
                if (!res.ok) {
                    if (res.status === 404) {
                        throw new Error('Case not found');
                    }
                    throw new Error('Failed to fetch case');
                }
                return res.json();
            })
            .then(data => {
                setCaseData(data);
            })
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    }, [id]);

    if (loading) {
        return (
            <div className="p-10 max-w-7xl mx-auto">
                <div className="text-center text-lg">Loading case details...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-10 max-w-7xl mx-auto">
                <div className="text-center text-red-600"><br/>Error: {error}</div>
            </div>
        );
    }

    if (!caseData) {
        return (
            <div className="p-10 max-w-7xl mx-auto">
                <div className="text-center text-lg">Case not found</div>
            </div>
        );
    }

    return (
        <div className="p-10 max-w-7xl mx-auto flex flex-col gap-10">
            {/* Page Header */}
            <section className="flex justify-between items-end">
                <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-on-surface-variant font-body text-sm uppercase tracking-widest">
                        <Link to="/cases" className="hover:text-primary transition-colors">Case Management</Link>
                        <span className="material-symbols-outlined text-[10px]">chevron_right</span>
                        <span className="text-primary font-bold">Matter #{caseData.case_id}</span>
                    </div>
                    <h1 className="font-headline font-extrabold text-4xl text-on-surface tracking-tight">{caseData.case_number || "N/A"} - {caseData.case_type || "Case"}</h1>
                </div>
                <div className="flex gap-3">
                    <button className="px-5 py-2.5 bg-secondary-container text-on-secondary-container rounded-md text-sm font-semibold flex items-center gap-2 hover:opacity-90 transition-all">
                        <span className="material-symbols-outlined text-sm">share</span>
                        Export
                    </button>
                    <button className="px-5 py-2.5 bg-primary text-on-primary rounded-md text-sm font-semibold shadow-lg shadow-primary/20 flex items-center gap-2 hover:opacity-90 transition-all">
                        <span className="material-symbols-outlined text-sm">save</span>
                        Save Changes
                    </button>
                </div>
            </section>

            {/* Content Grid */}
            <div className="grid grid-cols-12 gap-8">
                {/* Left Column: Case Details & History */}
                <div className="col-span-12 lg:col-span-8 flex flex-col gap-8">
                    {/* Case Overview Card */}
                    <div className="bg-surface-container-lowest p-8 rounded-xl shadow-sm flex flex-col gap-6">
                        <div className="flex justify-between items-center">
                            <h2 className="text-xl font-headline font-bold text-on-surface">Case Profile</h2>
                            <span className="px-3 py-1 bg-secondary-container text-on-secondary-container text-xs font-bold rounded-full">{caseData.status?.toUpperCase() || 'PENDING'}</span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <div>
                                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-wider mb-1 font-body">Filing Date</p>
                                <p className="text-sm font-medium text-on-surface font-body">{caseData.filing_date || 'N/A'}</p>
                            </div>
                            <div>
                                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-wider mb-1 font-body">Case Type</p>
                                <p className="text-sm font-medium text-on-surface font-body">{caseData.case_type || 'Not Specified'}</p>
                            </div>
                            <div>
                                <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-wider mb-1 font-body">Status</p>
                                <p className="text-sm font-medium text-on-surface font-body">{caseData.status || 'Unknown'}</p>
                            </div>
                        </div>
                        <div className="pt-4 border-t border-outline-variant/10">
                            <p className="text-[10px] text-on-surface-variant font-bold uppercase tracking-wider mb-2 font-body">Description</p>
                            <p className="text-sm text-on-surface leading-relaxed font-body">
                                {caseData.description || 'No description available'}
                            </p>
                        </div>
                    </div>

                    {/* Strategic Management */}
                    <div className="bg-surface-container-low p-8 rounded-xl flex flex-col gap-8">
                        <h2 className="text-xl font-headline font-bold text-on-surface">Case Management</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                            {/* Lawyer Assignment */}
                            <div className="flex flex-col gap-4">
                                <label className="text-sm font-bold text-on-surface">Assigned Counsel</label>
                                <div className="flex flex-col gap-3">
                                    {caseData.lawyer_name && caseData.lawyer_name !== 'Unassigned' ? (
                                        <div className="flex items-center gap-4 bg-surface-container-lowest p-3 rounded-lg border-l-4 border-primary">
                                            <div className="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center text-primary font-bold">
                                                {caseData.lawyer_name.charAt(0)}
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="text-sm font-semibold font-body">{caseData.lawyer_name}</span>
                                                <span className="text-xs text-on-surface-variant font-body">{caseData.lawyer_specialization || 'General Practice'}</span>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex items-center justify-center p-6 bg-surface-container-highest/30 rounded-lg text-on-surface-variant text-sm">No lawyer assigned</div>
                                    )}
                                </div>
                            </div>

                            {/* Client Info */}
                            <div className="flex flex-col gap-4">
                                <label className="text-sm font-bold text-on-surface">Client Information</label>
                                <div className="bg-surface-container-highest/30 p-4 rounded-lg flex flex-col gap-3">
                                    <p className="text-sm font-semibold font-body">{caseData.client_name}</p>
                                    <p className="text-xs text-on-surface-variant font-body">Email: {caseData.client_email || 'N/A'}</p>
                                    <p className="text-xs text-on-surface-variant font-body">Phone: {caseData.client_phone || 'N/A'}</p>
                                    <p className="text-xs text-on-surface-variant font-body">Address: {caseData.client_address || 'N/A'}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Client Context & Summary */}
                <div className="col-span-12 lg:col-span-4 flex flex-col gap-8">
                    {/* Case Summary Card */}
                    <div className="bg-surface-container p-6 rounded-xl flex flex-col gap-6">
                        <div>
                            <h3 className="font-headline font-bold text-lg">{caseData.case_number}</h3>
                            <span className="text-sm text-on-surface-variant font-body">Case ID: {caseData.case_id}</span>
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center py-2 border-b border-outline-variant/10">
                                <span className="text-xs text-on-surface-variant font-body">Status</span>
                                <span className={`text-sm font-bold ${caseData.status === 'Active' ? 'text-green-600' : caseData.status === 'Pending' ? 'text-yellow-600' : 'text-slate-600'}`}>{caseData.status}</span>
                            </div>
                            <div className="flex justify-between items-center py-2">
                                <span className="text-xs text-on-surface-variant font-body">Case Type</span>
                                <span className="text-sm font-bold font-body">{caseData.case_type || 'N/A'}</span>
                            </div>
                        </div>
                    </div>

                    {/* Quick Stats */}
                    <div className="bg-surface-container-low p-6 rounded-xl">
                        <h4 className="text-sm font-bold text-on-surface mb-4">Quick Details</h4>
                        <div className="text-xs space-y-3 text-on-surface-variant font-body">
                            <p><strong>Filed:</strong> {caseData.filing_date || 'Not specified'}</p>
                            <p><strong>Lawyer:</strong> {caseData.lawyer_name || 'Unassigned'}</p>
                            <p><strong>Client:</strong> {caseData.client_name || 'Unknown'}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CaseDetails;
