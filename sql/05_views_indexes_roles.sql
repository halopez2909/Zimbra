-- Zimbra Transactional System - Session 4
-- Developer: Andres Bautista - HU-03, HU-05, HU-08, HU-09
-- Views, Indexes and Concurrency Simulation

-- HT-S4-01: View - sales pipeline grouped by status
-- HU-09 - endpoint GET /views/pipeline

CREATE OR REPLACE VIEW vw_sales_pipeline AS
SELECT
    status,
    COUNT(*)::BIGINT AS total_proposals,
    COALESCE(SUM(proposed_amount), 0) AS total_amount,
    ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM sales_proposals), 0), 2) AS percentage
FROM sales_proposals
GROUP BY status
ORDER BY total_proposals DESC;

-- HT-S4-01: View - sales traceability from campaign to closed sale
-- HU-09 - endpoint GET /views/traceability

CREATE OR REPLACE VIEW vw_sales_traceability AS
SELECT
    s.sale_id,
    s.sale_date,
    c.full_name AS client_name,
    c.client_type,
    p.product_name,
    sp.proposed_amount,
    s.final_amount,
    s.payment_method,
    s.origin_channel,
    mc.campaign_name AS origin_campaign,
    mc.campaign_type,
    sel.full_name AS seller_name
FROM sales s
JOIN clients c ON c.client_id = s.client_id
JOIN products p ON p.product_id = s.product_id
JOIN sales_proposals sp ON sp.proposal_id = s.proposal_id
LEFT JOIN marketing_interactions mi ON mi.interaction_id = sp.interaction_id
LEFT JOIN marketing_campaigns mc ON mc.campaign_id = mi.campaign_id
LEFT JOIN sellers sel ON sel.seller_id = c.assigned_seller_id
ORDER BY s.sale_date DESC;

-- HT-S4-02: Indexes for interactions and proposals
-- HU-05/08 - Performance optimization

CREATE INDEX IF NOT EXISTS idx_interactions_score ON marketing_interactions(score);
CREATE INDEX IF NOT EXISTS idx_interactions_campaign ON marketing_interactions(campaign_id);
CREATE INDEX IF NOT EXISTS idx_interactions_client ON marketing_interactions(client_id);
CREATE INDEX IF NOT EXISTS idx_interactions_converted ON marketing_interactions(converted);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON sales_proposals(status);
CREATE INDEX IF NOT EXISTS idx_proposals_client ON sales_proposals(client_id);

-- HT-S4-03: Concurrency and locks simulation
-- HU-08/09 - ACID and concurrency control

-- Scenario 1: SELECT FOR UPDATE - exclusive lock
-- T1 locks proposal, T2 must wait until T1 commits
BEGIN;
SELECT * FROM sales_proposals WHERE proposal_id = 5 FOR UPDATE;
UPDATE sales_proposals SET notes = 'Locked by T1 - concurrency test' WHERE proposal_id = 5;
COMMIT;

-- Scenario 2: NOWAIT - fail immediately if row is locked
BEGIN;
SELECT * FROM sales_proposals WHERE proposal_id = 6 FOR UPDATE NOWAIT;
COMMIT;

-- Scenario 3: SKIP LOCKED - skip locked rows, process next available
BEGIN;
SELECT proposal_id, client_id, status FROM sales_proposals
WHERE status = 'draft'
FOR UPDATE SKIP LOCKED
LIMIT 1;
COMMIT;

-- Verify indexes with EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM marketing_interactions WHERE score >= 80;
EXPLAIN ANALYZE SELECT * FROM sales_proposals WHERE status = 'accepted';
EXPLAIN ANALYZE SELECT * FROM vw_sales_pipeline;
EXPLAIN ANALYZE SELECT * FROM vw_sales_traceability;

-- Verify created objects
SELECT table_name AS view_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
AND tablename IN ('marketing_interactions', 'sales_proposals')
ORDER BY tablename, indexname;

-- ==============================================-- ALEJA - HT-S4-05: Views for performance reports
-- HU-10 - Consolidated reporting
-- ==============================================
-- View: consolidated performance summary by period
CREATE OR REPLACE VIEW vw_performance_summary AS
SELECT
    period_start,
    period_end,
    total_visitors,
    total_downloads,
    total_prospects,
    total_proposals,
    total_sales,
    total_revenue,
    conversion_rate_pct,
    close_rate_pct
FROM performance_reports
ORDER BY period_start;

-- View: campaign effectiveness with conversion metrics
CREATE OR REPLACE VIEW vw_campaign_effectiveness AS
SELECT
    mc.campaign_id,
    mc.campaign_name,
    mc.campaign_type,
    mc.status,
    mc.budget,
    COUNT(mi.interaction_id)::BIGINT AS total_interactions,
    COALESCE(SUM(mi.converted), 0)::BIGINT AS total_converted,
    ROUND(COALESCE(SUM(mi.converted), 0) * 100.0 / NULLIF(COUNT(mi.interaction_id), 0), 2) AS conversion_rate,
    ROUND(mc.budget / NULLIF(SUM(mi.converted), 0), 2) AS cost_per_conversion
FROM marketing_campaigns mc
LEFT JOIN marketing_interactions mi ON mi.campaign_id = mc.campaign_id
GROUP BY mc.campaign_id, mc.campaign_name, mc.campaign_type, mc.status, mc.budget
ORDER BY conversion_rate DESC NULLS LAST;

-- ==============================================-- ALEJA - HT-S4-06: Roles and permissions
-- HU-02/04 - Security and access control
-- ==============================================
DROP ROLE IF EXISTS zimbra_admin;
CREATE ROLE zimbra_admin WITH LOGIN PASSWORD 'admin2026';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO zimbra_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO zimbra_admin;

DROP ROLE IF EXISTS zimbra_seller;
CREATE ROLE zimbra_seller WITH LOGIN PASSWORD 'seller2026';
GRANT SELECT ON clients, products, sales_proposals, marketing_campaigns, marketing_interactions TO zimbra_seller;
GRANT INSERT ON marketing_interactions, follow_ups, sales_proposals TO zimbra_seller;
GRANT UPDATE ON sales_proposals TO zimbra_seller;

DROP ROLE IF EXISTS zimbra_viewer;
CREATE ROLE zimbra_viewer WITH LOGIN PASSWORD 'viewer2026';
GRANT SELECT ON performance_reports TO zimbra_viewer;
GRANT SELECT ON vw_performance_summary TO zimbra_viewer;
GRANT SELECT ON vw_campaign_effectiveness TO zimbra_viewer;
GRANT SELECT ON vw_sales_pipeline TO zimbra_viewer;
GRANT SELECT ON vw_sales_traceability TO zimbra_viewer;

-- ==============================================-- ALEJA - HT-S4-07: Indexes for clients and campaigns
-- HU-02/04 - Performance optimization
-- ==============================================
CREATE INDEX IF NOT EXISTS idx_clients_type ON clients(client_type);
CREATE INDEX IF NOT EXISTS idx_clients_seller ON clients(assigned_seller_id);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON marketing_campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_type ON marketing_campaigns(campaign_type);

-- Verify Aleja objects
SELECT table_name AS view_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
AND tablename IN ('clients', 'marketing_campaigns')
ORDER BY tablename, indexname;

SELECT rolname, rolcanlogin
FROM pg_roles
WHERE rolname LIKE 'zimbra_%'
ORDER BY rolname;
-- Views, Indexes and Roles
-- ==============================================================-- Developer: Jenn Olaya - HT-S4-09 (views) and HT-S4-10 (indexes) - HU-06/07
-- ==============================================================
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
