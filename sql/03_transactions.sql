-- Zimbra Transactional System - Session 2
-- ACID Transactions, Savepoints and Error Simulation
-- Course: Transactional Systems - Uniminuto 2026
-- Developer: Andres Bautista - HU-03, HU-05, HU-08, HU-09

-- ============================================================
-- T1: Register interaction with lead scoring (HU-05)
-- If score >= 80, mark as converted and create sales alert
-- ============================================================
BEGIN;

INSERT INTO marketing_interactions (campaign_id, client_id, interaction_type, score, converted)
VALUES (3, 29, 'form_submission', 92, 1);

SAVEPOINT sp_interaction_created;

INSERT INTO sales_alerts (interaction_id, seller_id, alert_type, status)
VALUES (
    (SELECT interaction_id FROM marketing_interactions WHERE client_id = 29 AND campaign_id = 3 ORDER BY interaction_date DESC LIMIT 1),
    (SELECT assigned_seller_id FROM clients WHERE client_id = 29),
    'high_lead_score',
    'pending'
);

SAVEPOINT sp_alert_created;

COMMIT;

-- ============================================================
-- T2: Full sales pipeline - proposal creation (HU-08)
-- Creates proposal linked to marketing interaction
-- ============================================================
BEGIN;

SAVEPOINT sp_before_proposal;

INSERT INTO sales_proposals (client_id, product_id, interaction_id, num_users, proposed_amount, status, estimated_close_date, notes)
VALUES (
    29,
    4,
    (SELECT interaction_id FROM marketing_interactions WHERE client_id = 29 ORDER BY interaction_date DESC LIMIT 1),
    90,
    4500.00,
    'draft',
    '2026-06-01',
    'Proposal generated after high lead score alert'
);

SAVEPOINT sp_proposal_created;

-- Update proposal status to sent
UPDATE sales_proposals
SET status = 'sent'
WHERE client_id = 29 AND status = 'draft';

SAVEPOINT sp_proposal_sent;

-- Accept the proposal
UPDATE sales_proposals
SET status = 'accepted'
WHERE client_id = 29 AND status = 'sent';

COMMIT;

-- ============================================================
-- T3: Register closed sale - HU-09
-- Verifies proposal is accepted before creating sale
-- Updates client type to commercial
-- ============================================================
BEGIN;

SAVEPOINT sp_before_sale;

INSERT INTO sales (proposal_id, client_id, product_id, final_amount, num_users, payment_method, origin_channel)
VALUES (
    (SELECT proposal_id FROM sales_proposals WHERE client_id = 29 AND status = 'accepted' LIMIT 1),
    29,
    4,
    4300.00,
    90,
    'wire_transfer',
    'email'
);

SAVEPOINT sp_sale_created;

-- HU-02: update client type to commercial after sale
UPDATE clients
SET client_type = 'commercial'
WHERE client_id = 29;

SAVEPOINT sp_client_updated;

-- Update performance report for current period
UPDATE performance_reports
SET total_sales = total_sales + 1,
    total_revenue = total_revenue + 4300.00,
    close_rate_pct = ROUND((total_sales + 1) * 100.0 / NULLIF(total_proposals, 0), 2)
WHERE period_start = '2026-04-01' AND period_end = '2026-04-30';

COMMIT;

-- ============================================================
-- T4: ROLLBACK simulation - duplicate sale error (HU-09)
-- Tries to create a second sale for same proposal
-- ============================================================
BEGIN;

SAVEPOINT sp_before_duplicate;

-- This will fail because proposal_id has UNIQUE constraint
-- Simulates error recovery with rollback
INSERT INTO sales (proposal_id, client_id, product_id, final_amount, num_users, payment_method, origin_channel)
VALUES (1, 3, 4, 4500.00, 80, 'wire_transfer', 'email');

-- If error occurs, rollback to savepoint
ROLLBACK TO SAVEPOINT sp_before_duplicate;

ROLLBACK;

-- ============================================================
-- T5: ROLLBACK simulation - invalid product price
-- Tries to create proposal with negative amount
-- ============================================================
BEGIN;

SAVEPOINT sp_before_invalid;

INSERT INTO sales_proposals (client_id, product_id, interaction_id, num_users, proposed_amount, status, estimated_close_date, notes)
VALUES (5, 4, NULL, 10, -500.00, 'draft', '2026-06-15', 'Invalid amount - should be rejected');

SAVEPOINT sp_invalid_inserted;

-- Detect invalid data and rollback
ROLLBACK TO SAVEPOINT sp_before_invalid;

ROLLBACK;

-- ============================================================
-- T6: Batch product catalog update (HU-03)
-- Updates prices with savepoints per product type
-- ============================================================
BEGIN;

SAVEPOINT sp_before_price_update;

-- Apply 5% discount to cloud products
UPDATE products
SET base_price = ROUND(base_price * 0.95, 2)
WHERE product_name LIKE 'ZCS Cloud%';

SAVEPOINT sp_cloud_updated;

-- Apply 3% increase to enterprise products
UPDATE products
SET base_price = ROUND(base_price * 1.03, 2)
WHERE product_name LIKE 'ZCS Enterprise%';

SAVEPOINT sp_enterprise_updated;

COMMIT;

-- ============================================================
-- T7: Marketing campaign conversion tracking (HU-05)
-- Updates all interactions above threshold in a campaign
-- ============================================================
BEGIN;

SAVEPOINT sp_before_conversion;

UPDATE marketing_interactions
SET converted = 1
WHERE campaign_id = 3
AND score >= 80
AND converted = 0;

SAVEPOINT sp_conversions_updated;

-- Create alerts for newly converted interactions
INSERT INTO sales_alerts (interaction_id, seller_id, alert_type, status)
SELECT
    mi.interaction_id,
    c.assigned_seller_id,
    'high_lead_score',
    'pending'
FROM marketing_interactions mi
JOIN clients c ON c.client_id = mi.client_id
WHERE mi.campaign_id = 3
AND mi.converted = 1
AND mi.interaction_id NOT IN (SELECT interaction_id FROM sales_alerts);

COMMIT;

-- ============================================================
-- Verification queries
-- ============================================================

-- Check converted interactions by campaign
SELECT
    mc.campaign_name,
    COUNT(mi.interaction_id) AS total_interactions,
    SUM(mi.converted) AS total_converted,
    ROUND(SUM(mi.converted) * 100.0 / COUNT(mi.interaction_id), 2) AS conversion_rate
FROM marketing_interactions mi
JOIN marketing_campaigns mc ON mc.campaign_id = mi.campaign_id
GROUP BY mc.campaign_name
ORDER BY conversion_rate DESC;

-- Check full sales pipeline traceability
SELECT
    s.sale_id,
    c.full_name AS client,
    p.product_name,
    sp.proposed_amount,
    s.final_amount,
    s.payment_method,
    s.origin_channel,
    mc.campaign_name AS origin_campaign
FROM sales s
JOIN clients c ON c.client_id = s.client_id
JOIN products p ON p.product_id = s.product_id
JOIN sales_proposals sp ON sp.proposal_id = s.proposal_id
LEFT JOIN marketing_interactions mi ON mi.interaction_id = sp.interaction_id
LEFT JOIN marketing_campaigns mc ON mc.campaign_id = mi.campaign_id
ORDER BY s.sale_date DESC;

-- Check close rate per period
SELECT
    period_start,
    period_end,
    total_proposals,
    total_sales,
    close_rate_pct,
    total_revenue
FROM performance_reports
ORDER BY period_start;
