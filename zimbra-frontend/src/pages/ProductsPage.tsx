import { useEffect, useState } from 'react';
import { getProducts, createProduct, calculateAmount } from '../api/api';

export default function ProductsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [calcResult, setCalcResult] = useState<number | null>(null);
  const [form, setForm] = useState({ product_name: '', description: '', product_type: 'commercial', base_price: '', max_users: '' });
  const [calc, setCalc] = useState({ product_id: '', num_users: '' });

  const load = async () => {
    try { setProducts(await getProducts()); } catch { setError('Failed to load products'); }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(''); setSuccess('');
    try {
      await createProduct({ ...form, base_price: parseFloat(form.base_price), max_users: form.max_users ? parseInt(form.max_users) : null });
      setSuccess('Product created successfully');
      setForm({ product_name: '', description: '', product_type: 'commercial', base_price: '', max_users: '' });
      load();
    } catch (err: any) { setError(err.message); }
  };

  const handleCalculate = async (e: any) => {
    e.preventDefault();
    setError(''); setCalcResult(null);
    try {
      const res = await calculateAmount(parseInt(calc.product_id), parseInt(calc.num_users));
      setCalcResult(res.calculated_amount);
    } catch (err: any) { setError(err.message); }
  };

  return (
    <div style={{ padding: '24px' }}>
      <h1 style={{ color: '#1F3864', marginBottom: '12px' }}>Products</h1>
      <p style={{ color: '#666', marginTop: '12px', marginBottom: '24px' }}>ZCS product catalog</p>

      {error && <div style={{ background: '#FCE4D6', color: '#922B21', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{error}</div>}
      {success && <div style={{ background: '#E2EFDA', color: '#1E8449', padding: '10px', borderRadius: '6px', marginBottom: '16px' }}>{success}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Add Product</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Product Name *</label>
              <input value={form.product_name} onChange={e => setForm({ ...form, product_name: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Description</label>
              <input value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Type *</label>
              <select value={form.product_type} onChange={e => setForm({ ...form, product_type: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
                <option value="free">Free</option>
                <option value="commercial">Commercial</option>
              </select>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Base Price *</label>
              <input type="number" value={form.base_price} onChange={e => setForm({ ...form, base_price: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Max Users</label>
              <input type="number" value={form.max_users} onChange={e => setForm({ ...form, max_users: e.target.value })} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <button type="submit" style={{ background: '#2E75B6', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Create Product</button>
          </form>
        </div>

        <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
          <h3 style={{ marginTop: 0, color: '#1F3864' }}>Calculate Proposal Amount</h3>
          <form onSubmit={handleCalculate}>
            <div style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Product ID *</label>
              <input type="number" value={calc.product_id} onChange={e => setCalc({ ...calc, product_id: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Number of Users *</label>
              <input type="number" value={calc.num_users} onChange={e => setCalc({ ...calc, num_users: e.target.value })} required style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <button type="submit" style={{ background: '#1E8449', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', width: '100%' }}>Calculate Amount</button>
          </form>
          {calcResult !== null && (
            <div style={{ marginTop: '16px', background: '#E2EFDA', padding: '16px', borderRadius: '6px', textAlign: 'center' }}>
              <p style={{ margin: 0, fontSize: '14px', color: '#555' }}>Calculated Amount</p>
              <p style={{ margin: '4px 0 0', fontSize: '28px', fontWeight: 'bold', color: '#1E8449' }}></p>
            </div>
          )}
        </div>
      </div>

      <div style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px' }}>
        <h3 style={{ marginTop: 0, color: '#1F3864' }}>Product List ({products.length})</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#1F3864', color: '#fff' }}>
              <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Name</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Type</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Base Price</th>
              <th style={{ padding: '10px', textAlign: 'left' }}>Max Users</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p, i) => (
              <tr key={p.product_id} style={{ background: i % 2 === 0 ? '#f9f9f9' : '#fff' }}>
                <td style={{ padding: '10px' }}>{p.product_id}</td>
                <td style={{ padding: '10px' }}>{p.product_name}</td>
                <td style={{ padding: '10px' }}>
                  <span style={{ background: p.product_type === 'free' ? '#E2EFDA' : '#DEEAF1', color: p.product_type === 'free' ? '#1E8449' : '#1F3864', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' }}>
                    {p.product_type}
                  </span>
                </td>
                <td style={{ padding: '10px' }}>{Number(p.base_price).toLocaleString()}</td>
                <td style={{ padding: '10px' }}>{p.max_users ?? 'Unlimited'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
