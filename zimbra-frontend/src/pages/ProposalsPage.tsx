import { useEffect, useState } from 'react';
import { getProposals, createProposal, calculateAmount, getPipeline } from '../api/api';

export default function ProposalsPage() {
  const [proposals, setProposals] = useState<any[]>([]);
  const [pipeline, setPipeline] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [form, setForm] = useState({ client_id: '', product_id: '', num_users: '', interaction_id: '', status: 'draft', estimated_close_date: '', notes: '', proposed_amount: '' });

  const load = async () => {
    try {
      setProposals(await getProposals());
      setPipeline(await getPipeline());
    } catch { setError('Failed to load data'); }
  };

  useEffect(() => { load(); }, []);

  const handleCalculate = async () => {
    setError('');
    if (!form.product_id || !form.num_users) { setError('Enter product ID and number of users first'); return; }
    try {
      const res = await calculateAmount(parseInt(form.product_id), parseInt(form.num_users));
      setForm({ ...form, proposed_amount: res.calculated_amount.toString() });
    } catch (err: any) { setError(err.message); }
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(''); setSuccess('');
    try {
      await createProposal({
        client_id: parseInt(form.client_id),
        product_id: parseInt(form.product_id),
        num_users: parseInt(form.num_users),
        interaction_id: form.interaction_id ? parseInt(form.interaction_id) : null,
        status: form.status,
        estimated_close_date: form.estimated_close_date || null,
        notes: form.notes || null,
        proposed_amount: parseFloat(form.proposed_amount),
      });
      setSuccess('Proposal created successfully');
      setForm({ client_id: '', product_id: '', num_users: '', interaction_id: '', status: 'draft', estimated_close_date: '', notes: '', proposed_amount: '' });
      load();
    } catch (err: any) { setError(err.message); }
  };

  const statusColor: Record<string, string> = { draft: '#DEEAF1', sent: '#FFF2CC', negotiation: '#FCE4D6', accepted: '#E2EFDA', rejected: '#F2F2F2' };
  const statusText: Record<string, string> = { draft: '#1F3864', sent: '#7D6608', negotiation: '#922B21', accepted: '#1E8449', rejected: '#555' };
  const pipelineColor: Record<string, string> = { draft: '#2E75B6', sent: '#F39C12', negotiation: '#E67E22', accepted: '#1E8449', rejected: '#999' };

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '12px' }}>Proposals</h1>
      <p style={{ color: '#666', marginTop: '12px', marginBottom: '24px' }}>Sales pipeline management</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
        {pipeline.map(p => (
          <div key={p.status} style={{ background: '#fff', border: '2px solid ' + (pipelineColor[p.status] || '#ccc'), borderRadius: '8px', padding: '16px', minWidth: '150px', textAlign: 'center' }}>
            <p style={{ margin: 0, fontSize: '12px', color: '#666', textTransform: 'uppercase' }}>{p.status}</p>
            <p style={{ margin: '4px 0', fontSize: '24px', fontWeight: 'bold', color: pipelineColor[p.status] || '#333' }}>{p.total_proposals}</p>
            <p style={{ margin: 0, fontSize: '12px', color: '#888' }}></p>
            <p style={{ margin: '2px 0 0', fontSize: '11px', color: '#aaa' }}>{p.percentage}%</p>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '420px 1fr', gap: '24px' }}>
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Create Proposal</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Client ID *</label>
              <input type="number" value={form.client_id} onChange={e => setForm({ ...form, client_id: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Product ID *</label>
              <input type="number" value={form.product_id} onChange={e => setForm({ ...form, product_id: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Number of Users *</label>
              <input type="number" value={form.num_users} onChange={e => setForm({ ...form, num_users: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Proposed Amount *</label>
              <div style={{ display: 'flex', gap: '8px' }}>
                <input type="number" value={form.proposed_amount} onChange={e => setForm({ ...form, proposed_amount: e.target.value })} required style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} placeholder="Or click Calculate" />
                <button type="button" onClick={handleCalculate} style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '8px 12px', borderRadius: '4px', cursor: 'pointer', whiteSpace: 'nowrap' }}>Calculate</button>
              </div>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Interaction ID (optional)</label>
              <input type="number" value={form.interaction_id} onChange={e => setForm({ ...form, interaction_id: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Status *</label>
              <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
                <option value="draft">Draft</option>
                <option value="sent">Sent</option>
                <option value="negotiation">Negotiation</option>
              </select>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Estimated Close Date</label>
              <input type="date" value={form.estimated_close_date} onChange={e => setForm({ ...form, estimated_close_date: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Notes</label>
              <textarea value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} rows={2} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', resize: 'vertical' }} />
            </div>
            <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Create Proposal</button>
          </form>
        </div>

        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Proposals List ({proposals.length})</h3>
          <div style={{ overflowY: 'auto', maxHeight: '500px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#1F3864', color: '#fff' }}>
                  <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Client</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Product</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Users</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Amount</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Status</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Close Date</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {proposals.map((p, i) => (
                  <tr key={p.proposal_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                    <td style={{ padding: '8px' }}>{p.proposal_id}</td>
                    <td style={{ padding: '8px' }}>{p.client_id}</td>
                    <td style={{ padding: '8px' }}>{p.product_id}</td>
                    <td style={{ padding: '8px' }}>{p.num_users}</td>
                    <td style={{ padding: '8px', fontWeight: 'bold' }}>{'$' + Number(p.proposed_amount).toLocaleString()}</td>
                    <td style={{ padding: '8px' }}>
                      <span style={{ background: statusColor[p.status] || '#F2F2F2', color: statusText[p.status] || '#333', padding: '2px 8px', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold' }}>
                        {p.status}
                      </span>
                    </td>
                    <td style={{ padding: '8px', fontSize: '13px' }}>{p.estimated_close_date || '-'}</td>
                    <td style={{ padding: '8px' }}>
                      {p.status !== 'accepted' && p.status !== 'rejected' && (
                        <select
                          value={p.status}
                          onChange={async e => {
                            try {
                              await fetch('http://localhost:9000/proposals/' + p.proposal_id + '/status', {
                                method: 'PATCH',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ status: e.target.value })
                              });
                              setProposals(await getProposals());
                              setPipeline(await getPipeline());
                            } catch {}
                          }}
                          style={{ padding: '4px 8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '12px' }}
                        >
                          <option value="draft">Draft</option>
                          <option value="sent">Sent</option>
                          <option value="negotiation">Negotiation</option>
                          <option value="accepted">Accept</option>
                          <option value="rejected">Reject</option>
                        </select>
                      )}
                      {(p.status === 'accepted' || p.status === 'rejected') && (
                        <span style={{ fontSize: '12px', color: '#888' }}>{p.status}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
