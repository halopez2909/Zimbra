import { useState } from 'react';
import { getAlertsBySeller, updateAlertStatus, escalateAlerts } from '../api/api';

const statusColors: Record<string, { bg: string; fg: string }> = {
  pending: { bg: '#FCE4D6', fg: '#922B21' },
  in_management: { bg: '#FFF2CC', fg: '#9C6500' },
  attended: { bg: '#E2EFDA', fg: '#1E8449' },
  resolved: { bg: '#DEEAF1', fg: '#1F3864' },
  escalated: { bg: '#F8CBAD', fg: '#843C0C' },
};

export default function AlertsPage() {
  const [sellerId, setSellerId] = useState('');
  const [alerts, setAlerts] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loaded, setLoaded] = useState(false);

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
      load();
    } catch (err: any) { setError(err.message); }
  };

  const escalate = async () => {
    setError(''); setSuccess('');
    try {
      const res = await escalateAlerts();
      setSuccess('Escalated ' + res.escalated + ' overdue alert(s)');
      if (loaded) load();
    } catch (err: any) { setError(err.message); }
  };

  const pending = alerts.filter(a => a.status === 'pending');

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '4px' }}>Alerts</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>Pending sales alerts by seller and escalation (HU-06)</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px', marginBottom: '24px', display: 'flex', alignItems: 'flex-end', gap: '16px', flexWrap: 'wrap' }}>
        <form onSubmit={load} style={{ display: 'flex', alignItems: 'flex-end', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Seller ID *</label>
            <input type="number" value={sellerId} onChange={e => setSellerId(e.target.value)} required style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '140px' }} />
          </div>
          <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer' }}>Load Alerts</button>
        </form>
        <button onClick={escalate} style={{ background: '#C0504D', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', marginLeft: 'auto' }}>
          Escalate Overdue
        </button>
      </div>

      {loaded && (
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>
            Alerts for seller {sellerId} ({alerts.length} total, {pending.length} pending)
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
                  const c = statusColors[a.status] || { bg: '#eee', fg: '#333' };
                  return (
                    <tr key={a.alert_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                      <td style={{ padding: '10px' }}>{a.alert_id}</td>
                      <td style={{ padding: '10px' }}>{a.interaction_id}</td>
                      <td style={{ padding: '10px' }}>{a.alert_type}</td>
                      <td style={{ padding: '10px' }}>{a.alert_date ? new Date(a.alert_date).toLocaleDateString() : '-'}</td>
                      <td style={{ padding: '10px' }}>
                        <span style={{ background: c.bg, color: c.fg, padding: '2px 8px', borderRadius: '12px', fontSize: '12px' }}>{a.status}</span>
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
