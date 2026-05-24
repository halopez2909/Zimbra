f = open('sql/05_views_indexes_roles.sql', 'w', encoding='utf-8')
D = chr(36) + chr(36)
f.write("""-- Zimbra Transactional System - Session 4
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
""")
f.close()
print('OK')
