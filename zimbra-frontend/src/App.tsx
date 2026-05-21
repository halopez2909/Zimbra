import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import ProductsPage from './pages/ProductsPage';
import InteractionsPage from './pages/InteractionsPage';
import ProposalsPage from './pages/ProposalsPage';
import SellersPage from './pages/SellersPage';
import AlertsPage from './pages/AlertsPage';
import FollowUpsPage from './pages/FollowUpsPage';

const navStyle = { display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 16px', borderRadius: '6px', textDecoration: 'none', fontSize: '14px', color: '#fff', fontWeight: '500' };
const activeStyle = { background: 'rgba(255,255,255,0.2)' };

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'Inter, Segoe UI, sans-serif' }}>
        <div style={{ width: '220px', background: '#1F3864', display: 'flex', flexDirection: 'column', padding: '20px 12px', position: 'fixed', top: 0, left: 0, bottom: 0 }}>
          <div style={{ marginBottom: '32px', padding: '0 4px' }}>
            <h2 style={{ color: '#fff', margin: 0, fontSize: '18px' }}>Zimbra</h2>
            <p style={{ color: '#AABBEE', margin: '4px 0 0', fontSize: '11px' }}>Transactional System</p>
          </div>
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <NavLink to="/products" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Products
            </NavLink>
            <NavLink to="/interactions" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Interactions
            </NavLink>
            <NavLink to="/proposals" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Proposals
            </NavLink>
            <NavLink to="/sellers" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Sellers
            </NavLink>
            <NavLink to="/alerts" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Alerts
            </NavLink>
            <NavLink to="/followups" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>
              Follow-ups
            </NavLink>
          </nav>
          <div style={{ marginTop: 'auto', padding: '12px 4px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
            <p style={{ color: '#AABBEE', fontSize: '11px', margin: 0 }}>Zimbra Team - Uniminuto 2026</p>
            <p style={{ color: '#7788AA', fontSize: '10px', margin: '2px 0 0' }}>Sellers / Alerts / Follow-ups by Jenn Olaya</p>
          </div>
        </div>

        <div style={{ marginLeft: '220px', flex: 1, background: '#F5F7FA', minHeight: '100vh' }}>
          <Routes>
            <Route path="/" element={
              <div style={{ padding: '40px', textAlign: 'center' }}>
                <h1 style={{ color: '#1F3864' }}>Zimbra Transactional System</h1>
                <p style={{ color: '#666' }}>Session 3 - Marketing Engine and Sales Pipeline</p>
                <p style={{ color: '#888', fontSize: '14px' }}>Select a module from the sidebar to get started.</p>
              </div>
            } />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/interactions" element={<InteractionsPage />} />
            <Route path="/proposals" element={<ProposalsPage />} />
            <Route path="/sellers" element={<SellersPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/followups" element={<FollowUpsPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
