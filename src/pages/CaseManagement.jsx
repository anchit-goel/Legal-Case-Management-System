import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const STATUS_OPTIONS = [
  'Active',
  'Pending',
  'Closed',
];

const CaseRow = ({ c, onStatusUpdate, updating }) => {
  return (
    <tr className="group hover:bg-surface-container-low transition-colors">
      <td className="px-6 py-6 font-manrope font-bold text-primary">
        <Link to={`/cases/${c.case_id}`} className="hover:underline">#{c.case_id}</Link>
      </td>
      <td className="px-6 py-6">
        <div className="flex flex-col">
          <span className="font-bold text-on-surface">{c.client_name}</span>
        </div>
      </td>
      <td className="px-6 py-6">
        <span className="text-sm font-medium font-body">{c.lawyer_name || '-'}</span>
      </td>
      <td className="px-6 py-6">
        <span className="text-sm font-semibold font-body">N/A</span>
      </td>
      <td className="px-6 py-6">
        <span className={`px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-tight ${
          c.status === 'Active' ? 'bg-green-100 text-green-700' :
          c.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
          'bg-slate-100 text-slate-600'
        }`}>
          {c.status}
        </span>
      </td>
      <td className="px-6 py-6 text-right">
        <select
          className="mr-2 px-2 py-1 rounded border text-xs"
          value={c.status || "Pending"}
          disabled={updating}
          onChange={e => onStatusUpdate(c.case_id, e.target.value)}
        >
          {STATUS_OPTIONS.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
        <button
          className="p-2 rounded-lg hover:bg-surface-container-high transition-all text-xs font-bold"
          onClick={() => onStatusUpdate(c.case_id, c.status)}
          disabled={updating}
        >
          {updating ? 'Updating...' : 'Update'}
        </button>
      </td>
    </tr>
  );
};

const CaseManagement = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);

  const fetchCases = () => {
    setLoading(true);
    setError(null);
    fetch(`${import.meta.env.VITE_BACKEND_URL || '/api'}/cases`)
      .then(async res => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Failed to fetch cases");
        return data;
     })
      .then(data => setCases(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchCases();
  }, []);

  const handleStatusUpdate = (caseId, status) => {
    setUpdatingId(caseId);
    fetch(`${import.meta.env.VITE_BACKEND_URL || '/api'}/cases/${caseId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to update status');
        return res.json();
      })
      .then(() => fetchCases())
      .catch(err => setError(err.message))
      .finally(() => setUpdatingId(null));
  };

  return (
    <div className="pt-8 px-10 pb-16 max-w-[1440px] mx-auto">
      <div className="flex items-end justify-between mb-10">
        <div>
          <h2 className="text-4xl font-extrabold font-headline tracking-tight text-on-surface mb-2">Case Management</h2>
          <p className="text-on-surface-variant font-body flex items-center gap-2">
            <span className="w-2 h-2 bg-primary rounded-full"></span>
            {`Currently managing ${cases.length} active high-priority matters`}
          </p>
        </div>
        <div className="flex gap-2 p-1 bg-surface-container-low rounded-xl">
          <button className="px-4 py-2 text-sm font-semibold rounded-lg bg-white shadow-sm text-primary">Active Cases</button>
          <button className="px-4 py-2 text-sm font-semibold rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors">Archived</button>
          <button className="px-4 py-2 text-sm font-semibold rounded-lg text-on-surface-variant hover:bg-surface-container-high transition-colors">Templates</button>
        </div>
      </div>

      <div className="mb-6 flex flex-wrap items-center gap-4">
        <div className="flex-1 flex gap-2">
          <div className="px-4 py-2 bg-surface-container-lowest rounded-xl flex items-center gap-2 text-xs font-semibold text-secondary shadow-sm cursor-pointer hover:bg-surface-container-low transition-colors">
            <span className="material-symbols-outlined text-sm">filter_list</span>
            Status: All
            <span className="material-symbols-outlined text-sm">expand_more</span>
          </div>
          <div className="px-4 py-2 bg-surface-container-lowest rounded-xl flex items-center gap-2 text-xs font-semibold text-secondary shadow-sm cursor-pointer hover:bg-surface-container-low transition-colors">
            <span className="material-symbols-outlined text-sm">person</span>
            Attorney: Any
            <span className="material-symbols-outlined text-sm">expand_more</span>
          </div>
          <div className="px-4 py-2 bg-surface-container-lowest rounded-xl flex items-center gap-2 text-xs font-semibold text-secondary shadow-sm cursor-pointer hover:bg-surface-container-low transition-colors">
            <span className="material-symbols-outlined text-sm">event</span>
            Date Range
            <span className="material-symbols-outlined text-sm">expand_more</span>
          </div>
        </div>
        <div className="text-[11px] font-bold text-outline-variant uppercase tracking-tighter">
          Showing 1-{cases.length} of {cases.length}
        </div>
      </div>

      <div className="bg-surface-container-lowest rounded-2xl overflow-hidden shadow-sm shadow-slate-200/50">
        {loading ? (
          <div className="p-8 text-center text-lg">Loading cases...</div>
        ) : error ? (
          <div className="p-8 text-center text-red-600">{error}</div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container-low">
                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Case ID</th>
                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Client Name</th>
                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Assigned Lawyer</th>
                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Next Hearing</th>
                <th className="px-6 py-4 text-[11px] font-extrabold uppercase tracking-widest text-secondary/60 font-headline">Status</th>
                <th className="px-6 py-4 text-right"></th>
              </tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <CaseRow
                  key={c.case_id}
                  c={c}
                  onStatusUpdate={handleStatusUpdate}
                  updating={updatingId === c.case_id}
                />
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default CaseManagement;
