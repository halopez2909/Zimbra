f = open('src/pages/CampaignsPage.tsx', 'w', encoding='utf-8')
f.write('''import { useEffect, useState } from "react";
import { getCampaigns, createCampaign, getCampaignStats } from "../api/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [stats, setStats] = useState<Record<number, any>>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({ campaign_name: "", campaign_type: "email", objective: "acquisition", start_date: "", end_date: "", budget: "", status: "planned", tool: "OneView" });

  const load = async () => {
    try {
      const data = await getCampaigns();
      setCampaigns(data);
      const statsMap: Record<number, any> = {};
      for (const c of data) {
        try {
          statsMap[c.campaign_id] = await getCampaignStats(c.campaign_id);
        } catch { statsMap[c.campaign_id] = null; }
      }
      setStats(statsMap);
    } catch { setError("Failed to load campaigns"); }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(""); setSuccess("");
    try {
      await createCampaign({ ...form, budget: form.budget ? parseFloat(form.budget) : 0, end_date: form.end_date || null });
      setSuccess("Campaign created successfully");
      setForm({ campaign_name: "", campaign_type: "email", objective: "acquisition", start_date: "", end_date: "", budget: "", status: "planned", tool: "OneView" });
      load();
    } catch (err: any) { setError(err.message); }
  };

  const statusColor: Record<string, string> = { planned: "#FFF2CC", active: "#E2EFDA", finished: "#F2F2F2", cancelled: "#FCE4D6", high_demand: "#DEEAF1" };
  const statusText: Record<string, string> = { planned: "#7D6608", active: "#1E8449", finished: "#555", cancelled: "#922B21", high_demand: "#1F3864" };

  return (
    <div style={{ padding: "24px" }}>
      <h1 style={{ color: "#1F3864", marginBottom: "4px" }}>Campaigns</h1>
      <p style={{ color: "#666", marginBottom: "24px" }}>Marketing campaigns management - Heyleen Alejandra Lopez</p>

      {error && <div style={{ background: "#FCE4D6", color: "#922B21", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{error}</div>}
      {success && <div style={{ background: "#E2EFDA", color: "#1E8449", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{success}</div>}

      <div style={{ display: "grid", gridTemplateColumns: "380px 1fr", gap: "24px" }}>
        <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
          <h3 style={{ marginTop: 0, color: "#1F3864" }}>Create Campaign</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Campaign Name *</label>
              <input value={form.campaign_name} onChange={e => setForm({ ...form, campaign_name: e.target.value })} required style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Type *</label>
              <select value={form.campaign_type} onChange={e => setForm({ ...form, campaign_type: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}>
                <option value="email">Email</option>
                <option value="web_tracking">Web Tracking</option>
                <option value="lead_generation">Lead Generation</option>
                <option value="web">Web</option>
              </select>
            </div>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Objective *</label>
              <select value={form.objective} onChange={e => setForm({ ...form, objective: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}>
                <option value="acquisition">Acquisition</option>
                <option value="retention">Retention</option>
                <option value="reactivation">Reactivation</option>
                <option value="upselling">Upselling</option>
              </select>
            </div>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Start Date *</label>
              <input type="date" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} required style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>End Date</label>
              <input type="date" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Budget</label>
              <input type="number" value={form.budget} onChange={e => setForm({ ...form, budget: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Tool</label>
              <input value={form.tool} onChange={e => setForm({ ...form, tool: e.target.value })} style={{ width: "100%", padding: "8px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }} />
            </div>
            <button type="submit" style={{ background: "#2E75B6", color: "#fff", border: "none", padding: "10px 20px", borderRadius: "6px", cursor: "pointer", width: "100%" }}>Create Campaign</button>
          </form>
        </div>

        <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
          <h3 style={{ marginTop: 0, color: "#1F3864" }}>Campaign List ({campaigns.length})</h3>
          <div style={{ overflowY: "auto", maxHeight: "600px" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#1F3864", color: "#fff" }}>
                  {["ID", "Name", "Type", "Status", "Conversion", "Cost/Conv"].map(h => (
                    <th key={h} style={{ padding: "10px", textAlign: "left" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {campaigns.map((c, i) => (
                  <tr key={c.campaign_id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "#fff" }}>
                    <td style={{ padding: "8px" }}>{c.campaign_id}</td>
                    <td style={{ padding: "8px", fontSize: "13px" }}>{c.campaign_name}</td>
                    <td style={{ padding: "8px", fontSize: "12px" }}>{c.campaign_type}</td>
                    <td style={{ padding: "8px" }}>
                      <span style={{ background: statusColor[c.status] || "#F2F2F2", color: statusText[c.status] || "#333", padding: "2px 8px", borderRadius: "12px", fontSize: "12px", fontWeight: "bold" }}>
                        {c.status}
                      </span>
                    </td>
                    <td style={{ padding: "8px" }}>
                      {stats[c.campaign_id] ? (
                        <span style={{ color: "#1E8449", fontWeight: "bold" }}>{stats[c.campaign_id].conversion_rate}%</span>
                      ) : "-"}
                    </td>
                    <td style={{ padding: "8px", fontSize: "13px" }}>
                      {stats[c.campaign_id]?.cost_per_conversion ? "$" + stats[c.campaign_id].cost_per_conversion : "-"}
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
''')
f.close()
print('OK')
