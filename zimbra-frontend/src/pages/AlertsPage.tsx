import { useEffect, useState } from 'react';
import { getAlertsBySeller, updateAlertStatus, escalateAlerts, fetchPendingAlerts } from '../api/api';

const statusColors: Record<string, { bg: string; fg: string }> = {
  pending: { bg: '#FCE4D6', fg: '#922B21' },
  in_management: { bg: '#FFF2CC', fg: '#9C6500' },
  attended: { bg: '#E2EFDA', fg: '#1E8449' },
  resolved: { bg: '#DEEAF1', fg: '#1F3864' },
  escalated: { bg: '#F8CBAD', fg: '#843C0C' },
};

// urgency by alert age: red > 24h, yellow > 12h, otherwise neutral
function urgency(alertDate: string) {
  const hours = (Date.now() - new Date(alertDate).getTime()) / 36e5;
  if (hours > 24) return { color: '#C0504D', label: 'High', hours };
  if (hours > 12) return { color: '#C9A227', label: 'Medium', hours };
  return { color: '#1E8449', label: 'Low', hours };
}

export default function AlertsPage() {
  const [sellerId, setSellerId] = useState('');
  const [alerts, setAlerts] = useState<any[]>([]);
  const [pending, setPending] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loaded, setLoaded] = useState(false);

  const loadPending = async () => {
    try { setPending(await fetchPendingAlerts()); } catch { /* optional */ }
  };

  useEffect(() => { loadPending(); }, []);

  const load = async (e?: any) => {
    if (e) e.preventDefault();
    setError(''); setSuccess('');
    if (!sellerId) { setError('Enter a seller id'); return; }
    try {
      const data = await getAlertsBySeller(parseInt(sellerId));
      setAlerts(data);
      setLoaded(true);
    } catch (err: any) { setError(err.message); }
  };

  const attend = async (alertId: number) => {
    setError(''); setSuccess('');
    try {
      await updateAlertStatus(alertId, 'attended');
      setSuccess('Alert ' + alertId + ' marked as attended');
      if (loaded) load();
      loadPending();
    } catch (err: any) { setError(err.message); }
  };

  const escalate = async () => {
    setError(''); setSuccess('');
    try {
      const res = await escalateAlerts();
      setSuccess('Escalated ' + res.escalated + ' overdue alert(s)');
      if (loaded) load();
      loadPending();
    } catch (err: any) { setError(err.message); }
  };

  const localPending = alerts.filter(a => a.status === 'pending');

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '4px' }}>Alerts</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>Global pending alerts, per-seller view and escalation (HU-06)</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      {/* HT-S4-11: all pending alerts (vw_pending_alerts), oldest first with urgency */}
      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <h3 style={{ margin: 0, color: '#1F3864' }}>All Pending Alerts ({pending.length})</h3>
          <button onClick={escalate} style={{ background: '#C0504D', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' }}>Escalate Overdue</button>
        </div>
        {pending.length === 0 && <p style={{ color: '#888', fontSize: '14px' }}>No pending alerts in the system.</p>}
        {pending.length > 0 && (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#1F3864', color: '#fff' }}>
                <th style={{ padding: '10px', textAlign: 'left' }}>Urgency</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Seller</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Client</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Type</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Date</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {pending.map((a, i) => {
                const u = urgency(a.alert_date);
                return (
                  <tr key={a.alert_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                    <td style={{ padding: '10px' }}>
                      <span title={u.label} style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: u.color, marginRight: '6px', verticalAlign: 'middle' }} />
                      <span style={{ fontSize: '12px', color: u.color }}>{u.label}</span>
                    </td>
                    <td style={{ padding: '10px' }}>{a.alert_id}</td>
                    <td style={{ padding: '10px' }}>{a.seller_name}</td>
                    <td style={{ padding: '10px' }}>{a.client_name}</td>
                    <td style={{ padding: '10px' }}>{a.alert_type}</td>
                    <td style={{ padding: '10px' }}>{a.alert_date ? new Date(a.alert_date).toLocaleString() : '-'}</td>
                    <td style={{ padding: '10px' }}>
                      <button onClick={() => attend(a.alert_id)} style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}>Attend</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Per-seller view (kept from Session 3) */}
      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px', marginBottom: '24px' }}>
        <h3 style={{ marginTop: 0, color: '#1F3864' }}>Alerts by Seller</h3>
        <form onSubmit={load} style={{ display: 'flex', alignItems: 'flex-end', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Seller ID *</label>
            <input type="number" value={sellerId} onChange={e => setSellerId(e.target.value)} required style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '140px' }} />
          </div>
          <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' }}>Load Alerts</button>
        </form>
      </div>

      {loaded && (
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>
            Seller {sellerId} ({alerts.length} total, {localPending.length} pending)
          </h3>
          {alerts.length === 0 && <p style={{ color: '#888' }}>No alerts for this seller.</p>}
          {alerts.length > 0 && (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#1F3864', color: '#fff' }}>
                  <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Interaction</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Type</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Date</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Status</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((a, i) => {
                  const cc = statusColors[a.status] || { bg: '#eee', fg: '#333' };
                  return (
                    <tr key={a.alert_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                      <td style={{ padding: '10px' }}>{a.alert_id}</td>
                      <td style={{ padding: '10px' }}>{a.interaction_id}</td>
                      <td style={{ padding: '10px' }}>{a.alert_type}</td>
                      <td style={{ padding: '10px' }}>{a.alert_date ? new Date(a.alert_date).toLocaleDateString() : '-'}</td>
                      <td style={{ padding: '10px' }}>
                        <span style={{ background: cc.bg, color: cc.fg, padding: '2px 8px', borderRadius: '12px', fontSize: '12px' }}>{a.status}</span>
                      </td>
                      <td style={{ padding: '10px' }}>
                        {a.status === 'pending' ? (
                          <button onClick={() => attend(a.alert_id)} style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}>Attend</button>
                        ) : <span style={{ color: '#999', fontSize: '13px' }}>-</span>}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
