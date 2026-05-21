content = """-- Zimbra Transactional System - Session 3
-- Triggers, Stored Procedures and UDF Functions
-- Developer: Andres Bautista - HU-03, HU-05, HU-08, HU-09
-- Course: Transactional Systems - Uniminuto 2026

-- Trigger 1: auto-generate sales alert when lead score >= 80
-- HU-05 - fires after insert on marketing_interactions

CREATE OR REPLACE FUNCTION trg_fn_auto_alert()
RETURNS TRIGGER AS \\$
DECLARE
    v_seller_id INT;
BEGIN
    IF NEW.score >= 80 THEN
        SELECT assigned_seller_id INTO v_seller_id
        FROM clients
        WHERE client_id = NEW.client_id;

        IF v_seller_id IS NOT NULL THEN
            INSERT INTO sales_alerts (interaction_id, seller_id, alert_type, status)
            VALUES (NEW.interaction_id, v_seller_id, 'high_lead_score', 'pending');
        END IF;

        UPDATE marketing_interactions
        SET converted = 1
        WHERE interaction_id = NEW.interaction_id;
    END IF;
    RETURN NEW;
END;
\\$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auto_alert ON marketing_interactions;
CREATE TRIGGER trg_auto_alert
AFTER INSERT ON marketing_interactions
FOR EACH ROW
EXECUTE FUNCTION trg_fn_auto_alert();

-- Trigger 2: auto-create sale when proposal is accepted
-- HU-08 - fires after update on sales_proposals

CREATE OR REPLACE FUNCTION trg_fn_auto_sale()
RETURNS TRIGGER AS \\$
DECLARE
    v_existing INT;
BEGIN
    IF NEW.status = 'accepted' AND OLD.status != 'accepted' THEN
        SELECT COUNT(*) INTO v_existing
        FROM sales
        WHERE proposal_id = NEW.proposal_id;

        IF v_existing = 0 THEN
            INSERT INTO sales (proposal_id, client_id, product_id, final_amount, num_users, payment_method, origin_channel)
            VALUES (NEW.proposal_id, NEW.client_id, NEW.product_id, NEW.proposed_amount, NEW.num_users, 'wire_transfer', 'system');

            UPDATE clients
            SET client_type = 'commercial'
            WHERE client_id = NEW.client_id;
        END IF;
    END IF;
    RETURN NEW;
END;
\\$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auto_sale ON sales_proposals;
CREATE TRIGGER trg_auto_sale
AFTER UPDATE ON sales_proposals
FOR EACH ROW
EXECUTE FUNCTION trg_fn_auto_sale();

-- Function: sales pipeline report grouped by status
-- HU-09 - endpoint GET /sales/pipeline

CREATE OR REPLACE FUNCTION fn_sales_pipeline()
RETURNS TABLE(
    status VARCHAR,
    total_proposals BIGINT,
    total_amount NUMERIC,
    percentage NUMERIC
) AS \\$
BEGIN
    RETURN QUERY
    SELECT
        sp.status,
        COUNT(*)::BIGINT AS total_proposals,
        COALESCE(SUM(sp.proposed_amount), 0) AS total_amount,
        ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM sales_proposals), 0), 2) AS percentage
    FROM sales_proposals sp
    GROUP BY sp.status
    ORDER BY total_proposals DESC;
END;
\\$ LANGUAGE plpgsql;

-- Function: calculate proposal amount from product price and num users
-- HU-03 - endpoint GET /products/{id}/calculate?num_users=X

CREATE OR REPLACE FUNCTION fn_calculate_proposal_amount(
    p_product_id INT,
    p_num_users INT
)
RETURNS NUMERIC AS \\$
DECLARE
    v_base_price NUMERIC;
BEGIN
    SELECT base_price INTO v_base_price
    FROM products
    WHERE product_id = p_product_id;

    IF v_base_price IS NULL THEN
        RETURN NULL;
    END IF;

    RETURN v_base_price * p_num_users;
END;
\\$ LANGUAGE plpgsql;

-- Function: campaign conversion rate - converted interactions over total
-- HU-05 - endpoint GET /campaigns/{id}/conversion-rate

CREATE OR REPLACE FUNCTION fn_campaign_conversion_rate(
    p_campaign_id INT
)
RETURNS NUMERIC AS \\$
DECLARE
    v_rate NUMERIC;
BEGIN
    SELECT ROUND(
        COALESCE(SUM(converted), 0) * 100.0 / NULLIF(COUNT(*), 0), 2
    ) INTO v_rate
    FROM marketing_interactions
    WHERE campaign_id = p_campaign_id;

    RETURN COALESCE(v_rate, 0.00);
END;
\\$ LANGUAGE plpgsql;

-- verify created objects
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_type, routine_name;

SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table;
"""

with open('sql/04_triggers_procedures.sql', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
