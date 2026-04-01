import React, { useEffect, useState } from 'react';
import { BASE_URL } from '../api/config';
import { Link } from 'react-router-dom';

const Clients = () => {
    const [clients, setClients] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchClients = () => {
        setLoading(true);
        setError(null);
        fetch(`${BASE_URL}/clients`)
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch clients');
                return res.json();
            })
            .then(data => setClients(data || []))
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchClients();
    }, []);

    return (
        <div className="pt-8 px-10 pb-16 max-w-[1440px] mx-auto">
            <div className="flex items-end justify-between mb-10">
                <div>
                    <h2 className="text-4xl font-extrabold font-headline tracking-tight text-on-surface mb-2">Clients</h2>
                    <p className="text-on-surface-variant font-body flex items-center gap-2">
                        <span className="w-2 h-2 bg-primary rounded-full"></span>
                        {`Registered clients: ${clients.length}`}
                    </p>
                </div>
                <Link 
                    to="/intake"
                    className="px-6 py-3 bg-primary text-on-primary rounded-lg font-bold text-sm shadow-lg hover:shadow-primary/20 transition-all flex items-center gap-2"
                >
                    <span className="material-symbols-outlined text-sm">person_add</span>
                    Add New Client
                </Link>
            </div>

            <div className="bg-surface-container-lowest rounded-2xl overflow-hidden shadow-sm shadow-slate-200/50">
                {loading ? (
                    <div className="p-8 text-center text-lg">Loading clients...</div>
                ) : error ? (
                    <div className="p-8 text-center text-red-600">{error}</div>
                ) : clients.length === 0 ? (
                    <div className="p-8 text-center text-on-surface-variant">
                        <p className="text-lg font-semibold mb-2">No clients yet</p>
                        <p className="text-sm">Add a new client to get started</p>
                    </div>
                ) : (
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-surface-container-low">
                                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Name</th>
                                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Email</th>
                                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Phone</th>
                                <th className="px-6 py-4 text-right"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {clients.map((client) => (
                                <tr key={client.client_id} className="group hover:bg-surface-container-low transition-colors border-t border-outline-variant/5">
                                    <td className="px-6 py-6 font-manrope font-bold text-primary">
                                        {client.first_name} {client.last_name}
                                    </td>
                                    <td className="px-6 py-6">
                                        <span className="text-sm font-medium font-body">{client.email || '-'}</span>
                                    </td>
                                    <td className="px-6 py-6">
                                        <span className="text-sm font-medium font-body">{client.phone || '-'}</span>
                                    </td>
                                    <td className="px-6 py-6 text-right">
                                        <button className="p-2 rounded-lg hover:bg-surface-container-high transition-all text-xs font-bold">
                                            <span className="material-symbols-outlined">more_vert</span>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default Clients;
