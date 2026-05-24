-- Zimbra Transactional System - Session 4
-- Views, Indexes and Roles
-- =====================================================================
-- Developer: Jenn Olaya - HT-S4-09 (views) and HT-S4-10 (indexes) - HU-06/07
-- =====================================================================

-- HT-S4-09  View: seller performance summary
-- One row per seller with alerts, attended alerts, follow-ups and attention rate.
-- Used by GET /views/sellers and the SellersPage ranking.

CREATE OR REPLACE VIEW vw_seller_performance AS
SELECT
    s.seller_id,
    s.full_name,
    COUNT(DISTINCT sa.alert_id) AS total_alerts,
    COUNT(DISTINCT CASE WHEN sa.status IN ('attended', 'escalated') THEN sa.alert_id END) AS attended_alerts,
    COUNT(DISTINCT fu.followup_id) AS total_followups,
    COALESCE(ROUND(
        COUNT(DISTINCT CASE WHEN sa.status IN ('attended', 'escalated') THEN sa.alert_id END) * 100.0
        / NULLIF(COUNT(DISTINCT sa.alert_id), 0), 2
    ), 0.00) AS attention_rate
FROM sellers s
LEFT JOIN sales_alerts sa ON sa.seller_id = s.seller_id
LEFT JOIN follow_ups fu ON fu.seller_id = s.seller_id
GROUP BY s.seller_id, s.full_name;

-- HT-S4-09  View: pending alerts ordered by age (oldest first)
-- Joins seller and client names. Used by GET /views/pending-alerts and AlertsPage.

CREATE OR REPLACE VIEW vw_pending_alerts AS
SELECT
    sa.alert_id,
    sa.interaction_id,
    sa.seller_id,
    sa.alert_date,
    sa.alert_type,
    sa.status,
    s.full_name AS seller_name,
    c.full_name AS client_name
FROM sales_alerts sa
JOIN sellers s ON s.seller_id = sa.seller_id
JOIN marketing_interactions mi ON mi.interaction_id = sa.interaction_id
JOIN clients c ON c.client_id = mi.client_id
WHERE sa.status = 'pending'
ORDER BY sa.alert_date ASC;

-- HT-S4-10  Indexes to optimize the most frequent lookups
-- Alerts: by seller (GET /alerts/seller/{id}), by status, by date (escalation/ordering).
-- Follow-ups: by client (GET /followups/client/{id}) and by seller (reports).

CREATE INDEX IF NOT EXISTS idx_alerts_seller    ON sales_alerts(seller_id);
CREATE INDEX IF NOT EXISTS idx_alerts_status     ON sales_alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_date       ON sales_alerts(alert_date);
CREATE INDEX IF NOT EXISTS idx_followups_client  ON follow_ups(client_id);
CREATE INDEX IF NOT EXISTS idx_followups_seller  ON follow_ups(seller_id);

-- verify objects created
SELECT table_name FROM information_schema.views
WHERE table_schema = 'public' AND table_name IN ('vw_seller_performance', 'vw_pending_alerts');

SELECT indexname, tablename FROM pg_indexes
WHERE schemaname = 'public' AND indexname LIKE 'idx_%'
ORDER BY tablename, indexname;
