import { useEffect, useState } from 'react';
import { getInteractions, createInteraction } from '../api/api';

export default function InteractionsPage() {
  const [interactions, setInteractions] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [alertMsg, setAlertMsg] = useState('');
  const [form, setForm] = useState({ campaign_id: '', client_id: '', interaction_type: 'web_visit', score: '0' });

  const load = async () => {
    try { setInteractions(await getInteractions()); } catch { setError('Failed to load interactions'); }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(''); setSuccess(''); setAlertMsg('');
    try {
      const res = await createInteraction({
        campaign_id: parseInt(form.campaign_id),
        client_id: parseInt(form.client_id),
        interaction_type: form.interaction_type,
        score: parseInt(form.score),
      });
      setSuccess('Interaction registered successfully');
      if (parseInt(form.score) >= 80) {
        setAlertMsg('Alert created automatically by trigger');
      } else {
        setAlertMsg('No alert generated - score below threshold');
      }
      setForm({ campaign_id: '', client_id: '', interaction_type: 'web_visit', score: '0' });
      load();
    } catch (err: any) { setError(err.message); }
  };

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '12px' }}>Interactions</h1>
      <p style={{ color: '#666', marginTop: '12px', marginBottom: '24px' }}>Marketing lead scoring</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '8px' }}>{success}</div>}
      {alertMsg && (
        <div style={{ background: parseInt(form.score) >= 80 || alertMsg.includes('automatically') ? '#E2EFDA' : '#F2F2F2', color: alertMsg.includes('automatically') ? '#1E8449' : '#555', padding: '10px', borderRadius: '6px', marginBottom: '16px', fontWeight: 'bold' }}>
          {alertMsg.includes('automatically') ? '🔔 ' : '⚪ '}{alertMsg}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '400px 1fr', gap: '24px', marginBottom: '32px' }}>
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Register Interaction</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Campaign ID *</label>
              <input type="number" value={form.campaign_id} onChange={e => setForm({ ...form, campaign_id: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Client ID *</label>
              <input type="number" value={form.client_id} onChange={e => setForm({ ...form, client_id: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Interaction Type *</label>
              <select value={form.interaction_type} onChange={e => setForm({ ...form, interaction_type: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
                <option value="web_visit">Web Visit</option>
                <option value="email_open">Email Open</option>
                <option value="trial_download">Trial Download</option>
                <option value="form_submission">Form Submission</option>
                <option value="click">Click</option>
              </select>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Score: {form.score} {parseInt(form.score) >= 80 ? '🔔' : ''}</label>
              <input type="range" min="0" max="100" value={form.score} onChange={e => setForm({ ...form, score: e.target.value })} style={{ width: '100%' }} />
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#888' }}>
                <span>0</span>
                <span style={{ color: parseInt(form.score) >= 80 ? '#1E8449' : '#888', fontWeight: parseInt(form.score) >= 80 ? 'bold' : 'normal' }}>
                  {parseInt(form.score) >= 80 ? 'Alert threshold reached!' : 'Alert threshold: 80'}
                </span>
                <span>100</span>
              </div>
            </div>
            <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Register Interaction</button>
          </form>
        </div>

        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Recent Interactions ({interactions.length})</h3>
          <div style={{ overflowY: 'auto', maxHeight: '400px' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#1F3864', color: '#fff' }}>
                  <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Campaign</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Client</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Type</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Score</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Converted</th>
                </tr>
              </thead>
              <tbody>
                {interactions.slice().reverse().slice(0, 20).map((i, idx) => (
                  <tr key={i.interaction_id} style={{ background: idx % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                    <td style={{ padding: '8px' }}>{i.interaction_id}</td>
                    <td style={{ padding: '8px' }}>{i.campaign_id}</td>
                    <td style={{ padding: '8px' }}>{i.client_id}</td>
                    <td style={{ padding: '8px', fontSize: '12px' }}>{i.interaction_type}</td>
                    <td style={{ padding: '8px' }}>
                      <span style={{ background: i.score >= 80 ? '#E2EFDA' : '#F2F2F2', color: i.score >= 80 ? '#1E8449' : '#555', padding: '2px 8px', borderRadius: '12px', fontSize: '12px', fontWeight: 'bold' }}>
                        {i.score}
                      </span>
                    </td>
                    <td style={{ padding: '8px' }}>
                      <span style={{ background: i.converted ? '#E2EFDA' : '#FCE4D6', color: i.converted ? '#1E8449' : '#922B21', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' }}>
                        {i.converted ? 'Yes' : 'No'}
                      </span>
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
