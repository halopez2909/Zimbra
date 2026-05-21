import { useEffect, useState } from 'react';
import { getSellers, createSeller, getSellerReport, getAlertRate, getFollowupSummary } from '../api/api';

export default function SellersPage() {
  const [sellers, setSellers] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [form, setForm] = useState({ full_name: '', email: '', phone: '' });
  const [report, setReport] = useState<any | null>(null);
  const [alertRate, setAlertRate] = useState<number | null>(null);
  const [summary, setSummary] = useState<any | null>(null);
  const [selected, setSelected] = useState<any | null>(null);

  const load = async () => {
    try { setSellers(await getSellers(true)); } catch { setError('Failed to load sellers'); }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(''); setSuccess('');
    try {
      await createSeller(form);
      setSuccess('Seller created successfully');
      setForm({ full_name: '', email: '', phone: '' });
      load();
    } catch (err: any) { setError(err.message); }
  };

  const viewReport = async (seller: any) => {
    setError(''); setReport(null); setAlertRate(null); setSummary(null);
    setSelected(seller);
    try {
      const [rep, rate, sum] = await Promise.all([
        getSellerReport(seller.seller_id),
        getAlertRate(seller.seller_id),
        getFollowupSummary(seller.seller_id),
      ]);
      setReport(rep);
      setAlertRate(rate.alert_response_rate);
      setSummary(sum);
    } catch (err: any) { setError(err.message); }
  };

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '4px' }}>Sellers</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>Sales team management and performance report (HU-01)</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Register Seller</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Full Name *</label>
              <input value={form.full_name} onChange={e => setForm({ ...form, full_name: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Email *</label>
              <input type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Phone</label>
              <input value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Create Seller</button>
          </form>
        </div>

        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Management Report</h3>
          {!report && <p style={{ color: '#888', fontSize: '14px' }}>Select "Report" on a seller to see their metrics.</p>}
          {report && (
            <div>
              <p style={{ margin: '0 0 12px', fontWeight: 'bold', color: '#1F3864' }}>{selected?.full_name} (ID {report.seller_id})</p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <Metric label="Total alerts" value={report.total_alerts} />
                <Metric label="Attended alerts" value={report.attended_alerts} />
                <Metric label="Follow-ups" value={report.total_followups} />
                <Metric label="Managed clients" value={report.managed_clients} />
                <Metric label="Attention rate" value={report.attention_rate + '%'} />
                <Metric label="Alert response rate" value={(alertRate ?? 0) + '%'} />
              </div>
              {summary && (
                <div style={{ marginTop: '14px', background: '#F5F7FA', borderRadius: '6px', padding: '12px', fontSize: '13px', color: '#444' }}>
                  <strong>Follow-up summary:</strong> {summary.total_followups} total,{' '}
                  {summary.pending_contacts} pending contacts, most used:{' '}
                  {summary.most_used_contact_type ?? '-'}, common result: {summary.most_common_result ?? '-'}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
        <h3 style={{ marginTop: 0, color: '#1F3864' }}>Seller List ({sellers.length})</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#1F3864', color: '#fff' }}>
              <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Name</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Email</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Phone</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {sellers.map((s, i) => (
              <tr key={s.seller_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                <td style={{ padding: '10px' }}>{s.seller_id}</td>
                <td style={{ padding: '10px' }}>{s.full_name}</td>
                <td style={{ padding: '10px' }}>{s.email}</td>
                <td style={{ padding: '10px' }}>{s.phone ?? '-'}</td>
                <td style={{ padding: '10px' }}>
                  <button onClick={() => viewReport(s)} style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '6px 14px', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' }}>Report</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: any }) {
  return (
    <div style={{ background: '#DEEAF1', borderRadius: '6px', padding: '10px', textAlign: 'center' }}>
      <p style={{ margin: 0, fontSize: '12px', color: '#555' }}>{label}</p>
      <p style={{ margin: '4px 0 0', fontSize: '20px', fontWeight: 'bold', color: '#1F3864' }}>{value}</p>
    </div>
  );
}
