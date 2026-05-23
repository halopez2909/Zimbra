import { useState } from "react";
import { getPerformanceReport } from "../api/api";

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [form, setForm] = useState({ start: "", end: "" });

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(""); setLoading(true);
    setSearched(true);
    try {
      const data = await getPerformanceReport(form.start, form.end);
      const unique = data.filter((r: any, i: number, arr: any[]) =>
        arr.findIndex((x: any) => x.period_start === r.period_start && x.period_end === r.period_end) === i
      );
      setReports(unique);
    } catch (err: any) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ padding: "24px" }}>
      <h1 style={{ color: "#1F3864", marginBottom: "12px" }}>Performance Reports</h1>
      <p style={{ color: "#666", marginTop: "10px", marginBottom: "24px" }}>Marketing and sales metrics by period - Heyleen Alejandra Lopez</p>

      {error && <div style={{ background: "#FCE4D6", color: "#922B21", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{error}</div>}

      <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginBottom: "24px" }}>
        <h3 style={{ marginTop: 0, color: "#1F3864" }}>Generate Report</h3>
        <form onSubmit={handleSubmit} style={{ display: "flex", gap: "16px", alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>Start Date *</label>
            <input type="date" value={form.start} onChange={e => setForm({ ...form, start: e.target.value })} required style={{ padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }} />
          </div>
          <div>
            <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>End Date *</label>
            <input type="date" value={form.end} onChange={e => setForm({ ...form, end: e.target.value })} required style={{ padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }} />
          </div>
          <button type="submit" style={{ background: "#2E75B6", color: "#fff", border: "none", padding: "10px 20px", borderRadius: "6px", cursor: "pointer" }}>
            {loading ? "Loading..." : "Generate Report"}
          </button>
        </form>
      </div>

      {reports.length > 0 && reports.map((r, i) => (
        <div key={i} style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginBottom: "16px" }}>
          <h3 style={{ marginTop: 0, color: "#1F3864" }}>Period: {r.period_start} to {r.period_end}</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px", marginBottom: "16px" }}>
            {[
              ["Visitors", r.total_visitors.toLocaleString(), "#2E75B6"],
              ["Downloads", r.total_downloads.toLocaleString(), "#1F3864"],
              ["Prospects", r.total_prospects, "#7D6608"],
              ["Proposals", r.total_proposals, "#E67E22"],
              ["Sales", r.total_sales, "#1E8449"],
            ].map(([label, value, color]) => (
              <div key={label as string} style={{ background: "#F5F7FA", borderRadius: "8px", padding: "16px", textAlign: "center" }}>
                <p style={{ margin: 0, fontSize: "12px", color: "#666" }}>{label as string}</p>
                <p style={{ margin: "4px 0 0", fontSize: "24px", fontWeight: "bold", color: color as string }}>{value as string}</p>
              </div>
            ))}
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px" }}>
            <div style={{ background: "#E2EFDA", borderRadius: "8px", padding: "16px", textAlign: "center" }}>
              <p style={{ margin: 0, fontSize: "12px", color: "#555" }}>Total Revenue</p>
              <p style={{ margin: "4px 0 0", fontSize: "22px", fontWeight: "bold", color: "#1E8449" }}>{"$" + Number(r.total_revenue).toLocaleString()}</p>
            </div>
            <div style={{ background: "#DEEAF1", borderRadius: "8px", padding: "16px", textAlign: "center" }}>
              <p style={{ margin: 0, fontSize: "12px", color: "#555" }}>Conversion Rate</p>
              <p style={{ margin: "4px 0 0", fontSize: "22px", fontWeight: "bold", color: "#2E75B6" }}>{r.conversion_rate_pct}%</p>
            </div>
            <div style={{ background: r.close_rate_pct < 10 ? "#FCE4D6" : "#E2EFDA", borderRadius: "8px", padding: "16px", textAlign: "center" }}>
              <p style={{ margin: 0, fontSize: "12px", color: "#555" }}>Close Rate</p>
              <p style={{ margin: "4px 0 0", fontSize: "22px", fontWeight: "bold", color: r.close_rate_pct < 10 ? "#922B21" : "#1E8449" }}>{r.close_rate_pct}%</p>
              {r.close_rate_pct < 10 && <p style={{ margin: "4px 0 0", fontSize: "11px", color: "#922B21" }}>Below target</p>}
            </div>
          </div>
        </div>
      ))}

      {reports.length === 0 && !loading && searched && (
        <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "40px", textAlign: "center", color: "#888" }}>
          No data found for the selected period.
        </div>
      )}
    </div>
  );
}
