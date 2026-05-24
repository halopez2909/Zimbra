f = open('sql/05_views_indexes_roles.sql', 'a', encoding='utf-8')
f.write("""
-- =====================================================
-- ALEJA - HT-S4-05: Views for performance reports
-- HU-10 - Consolidated reporting
-- =====================================================

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

-- =====================================================
-- ALEJA - HT-S4-06: Roles and permissions
-- HU-02/04 - Security and access control
-- =====================================================

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

-- =====================================================
-- ALEJA - HT-S4-07: Indexes for clients and campaigns
-- HU-02/04 - Performance optimization
-- =====================================================

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
""")
f.close()
print('OK')
