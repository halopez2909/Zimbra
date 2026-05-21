import { useState } from 'react';
import { createFollowUp, getFollowUpsByClient } from '../api/api';

export default function FollowUpsPage() {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [form, setForm] = useState({
    client_id: '', seller_id: '', alert_id: '', contact_type: 'call', result: '', notes: '', next_contact: '',
  });
  const [historyClientId, setHistoryClientId] = useState('');
  const [history, setHistory] = useState<any[]>([]);
  const [historyLoaded, setHistoryLoaded] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(''); setSuccess('');
    try {
      const payload: any = {
        client_id: parseInt(form.client_id),
        seller_id: parseInt(form.seller_id),
        contact_type: form.contact_type,
        alert_id: form.alert_id ? parseInt(form.alert_id) : null,
        result: form.result || null,
        notes: form.notes || null,
        next_contact: form.next_contact || null,
      };
      await createFollowUp(payload);
      setSuccess(
        form.alert_id
          ? 'Follow-up registered. Alert ' + form.alert_id + ' auto-marked as attended by the trigger.'
          : 'Follow-up registered successfully.'
      );
      setForm({ client_id: '', seller_id: '', alert_id: '', contact_type: 'call', result: '', notes: '', next_contact: '' });
      if (historyLoaded && historyClientId === payload.client_id.toString()) loadHistory();
    } catch (err: any) { setError(err.message); }
  };

  const loadHistory = async (e?: any) => {
    if (e) e.preventDefault();
    setError('');
    if (!historyClientId) { setError('Enter a client id'); return; }
    try {
      setHistory(await getFollowUpsByClient(parseInt(historyClientId)));
      setHistoryLoaded(true);
    } catch (err: any) { setError(err.message); }
  };

  const inputStyle = { width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' as const };

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '4px' }}>Follow-ups</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>Register commercial contacts. Linking an alert auto-attends it (HU-07)</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Register Follow-up</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Client ID *</label>
                <input type="number" value={form.client_id} onChange={e => setForm({ ...form, client_id: e.target.value })} required style={inputStyle} />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Seller ID *</label>
                <input type="number" value={form.seller_id} onChange={e => setForm({ ...form, seller_id: e.target.value })} required style={inputStyle} />
              </div>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Alert ID (optional - triggers auto-attend)</label>
              <input type="number" value={form.alert_id} onChange={e => setForm({ ...form, alert_id: e.target.value })} style={inputStyle} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Contact Type *</label>
              <select value={form.contact_type} onChange={e => setForm({ ...form, contact_type: e.target.value })} style={{ ...inputStyle }}>
                <option value="call">Call</option>
                <option value="email">Email</option>
                <option value="visit">Visit</option>
              </select>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Result</label>
              <input value={form.result} onChange={e => setForm({ ...form, result: e.target.value })} style={inputStyle} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Notes</label>
              <input value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} style={inputStyle} />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Next Contact</label>
              <input type="date" value={form.next_contact} onChange={e => setForm({ ...form, next_contact: e.target.value })} style={inputStyle} />
            </div>
            <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Register Follow-up</button>
          </form>
        </div>

        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Client History</h3>
          <form onSubmit={loadHistory} style={{ display: 'flex', alignItems: 'flex-end', gap: '12px', marginBottom: '16px' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Client ID *</label>
              <input type="number" value={historyClientId} onChange={e => setHistoryClientId(e.target.value)} required style={inputStyle} />
            </div>
            <button type="submit" style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' }}>Load</button>
          </form>
          {historyLoaded && history.length === 0 && <p style={{ color: '#888', fontSize: '14px' }}>No follow-ups for this client.</p>}
          {history.map(f => (
            <div key={f.followup_id} style={{ borderLeft: '3px solid #2E75B6', padding: '8px 12px', marginBottom: '8px', background: '#F5F7FA', borderRadius: '0 6px 6px 0' }}>
              <p style={{ margin: 0, fontSize: '13px', fontWeight: 'bold', color: '#1F3864' }}>
                {f.contact_type.toUpperCase()} {f.result ? '- ' + f.result : ''}
              </p>
              <p style={{ margin: '2px 0 0', fontSize: '12px', color: '#666' }}>{f.notes}</p>
              <p style={{ margin: '2px 0 0', fontSize: '11px', color: '#999' }}>
                {f.contact_date ? new Date(f.contact_date).toLocaleDateString() : ''}
                {f.alert_id ? ' - alert #' + f.alert_id : ''}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
