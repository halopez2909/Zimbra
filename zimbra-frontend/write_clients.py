f = open('src/pages/ClientsPage.tsx', 'w', encoding='utf-8')
f.write('''import { useEffect, useState } from "react";
import { getClients, createClient } from "../api/api";

export default function ClientsPage() {
  const [clients, setClients] = useState<any[]>([]);
  const [filter, setFilter] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({ full_name: "", company: "", email: "", phone: "", client_type: "prospect", assigned_seller_id: "" });

  const load = async (type?: string) => {
    try { setClients(await getClients(type || undefined)); } catch { setError("Failed to load clients"); }
  };

  useEffect(() => { load(); }, []);

  const handleFilter = (type: string) => { setFilter(type); load(type || undefined); };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(""); setSuccess("");
    try {
      await createClient({ ...form, assigned_seller_id: form.assigned_seller_id ? parseInt(form.assigned_seller_id) : null });
      setSuccess("Client created successfully");
      setForm({ full_name: "", company: "", email: "", phone: "", client_type: "prospect", assigned_seller_id: "" });
      load(filter || undefined);
    } catch (err: any) { setError(err.message); }
  };

  const typeColor: Record<string, string> = { prospect: "#FFF2CC", trial: "#DEEAF1", commercial: "#E2EFDA" };
  const typeText: Record<string, string> = { prospect: "#7D6608", trial: "#1F3864", commercial: "#1E8449" };

  return (
    <div style={{ padding: "24px" }}>
      <h1 style={{ color: "#1F3864", marginBottom: "4px" }}>Clients</h1>
      <p style={{ color: "#666", marginBottom: "24px" }}>Client funnel management - Heyleen Alejandra Lopez</p>

      {error && <div style={{ background: "#FCE4D6", color: "#922B21", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{error}</div>}
      {success && <div style={{ background: "#E2EFDA", color: "#1E8449", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{success}</div>}

      <div style={{ display: "flex", gap: "8px", marginBottom: "20px" }}>
        {["", "prospect", "trial", "commercial"].map(t => (
          <button key={t} onClick={() => handleFilter(t)} style={{ background: filter === t ? "#1F3864" : "#fff", color: filter === t ? "#fff" : "#333", border: "1px solid #ddd", padding: "6px 14px", borderRadius: "20px", cursor: "pointer", fontSize: "13px" }}>
            {t === "" ? "All" : t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "380px 1fr", gap: "24px" }}>
        <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
          <h3 style={{ marginTop: 0, color: "#1F3864" }}>Add Client</h3>
          <form onSubmit={handleSubmit}>
            {[["Full Name", "full_name", "text"], ["Company", "company", "text"], ["Email", "email", "email"], ["Phone", "phone", "text"]].map(([label, key, type]) => (
              <div key={key} style={{ marginBottom: "10px" }}>
                <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>{label} {key === "full_name" || key === "email" ? "*" : ""}</label>
                <input type={type} value={(form as any)[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} required={key === "full_name" || key === "email"} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
              </div>
            ))}
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Client Type *</label>
              <select value={form.client_type} onChange={e => setForm({ ...form, client_type: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}>
                <option value="prospect">Prospect</option>
                <option value="trial">Trial</option>
                <option value="commercial">Commercial</option>
              </select>
            </div>
            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Seller ID (optional)</label>
              <input type="number" value={form.assigned_seller_id} onChange={e => setForm({ ...form, assigned_seller_id: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <button type="submit" style={{ background: "#2E75B6", color: "#fff", border: "none", padding: "10px 20px", borderRadius: "6px", cursor: "pointer", width: "100%" }}>Create Client</button>
          </form>
        </div>

        <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
          <h3 style={{ marginTop: 0, color: "#1F3864" }}>Client List ({clients.length})</h3>
          <div style={{ overflowY: "auto", maxHeight: "500px" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#1F3864", color: "#fff" }}>
                  {["ID", "Name", "Company", "Email", "Type", "Seller"].map(h => (
                    <th key={h} style={{ padding: "10px", textAlign: "left" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {clients.map((c, i) => (
                  <tr key={c.client_id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "#fff" }}>
                    <td style={{ padding: "8px" }}>{c.client_id}</td>
                    <td style={{ padding: "8px" }}>{c.full_name}</td>
                    <td style={{ padding: "8px", fontSize: "13px" }}>{c.company || "-"}</td>
                    <td style={{ padding: "8px", fontSize: "12px" }}>{c.email}</td>
                    <td style={{ padding: "8px" }}>
                      <span style={{ background: typeColor[c.client_type] || "#F2F2F2", color: typeText[c.client_type] || "#333", padding: "2px 8px", borderRadius: "12px", fontSize: "12px", fontWeight: "bold" }}>
                        {c.client_type}
                      </span>
                    </td>
                    <td style={{ padding: "8px" }}>{c.assigned_seller_id || "-"}</td>
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
''')
f.close()
print('OK')
