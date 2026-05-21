-- Zimbra Transactional System - Session 3
-- Triggers, Stored Procedures and UDF Functions
-- Developer: Andres Bautista - HU-03, HU-05, HU-08, HU-09

-- Trigger 1: auto-generate sales alert when lead score >= 80
-- HU-05 - fires after insert on marketing_interactions

CREATE OR REPLACE FUNCTION trg_fn_auto_alert()
RETURNS TRIGGER AS $$
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
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_auto_alert ON marketing_interactions;
CREATE TRIGGER trg_auto_alert
AFTER INSERT ON marketing_interactions
FOR EACH ROW
EXECUTE FUNCTION trg_fn_auto_alert();

-- Trigger 2: auto-create sale when proposal is accepted
-- HU-08 - fires after update on sales_proposals

CREATE OR REPLACE FUNCTION trg_fn_auto_sale()
RETURNS TRIGGER AS $$
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
$$ LANGUAGE plpgsql;

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
) AS $$
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
$$ LANGUAGE plpgsql;

-- Function: calculate proposal amount from product price and num users
-- HU-03 - endpoint GET /products/{id}/calculate?num_users=X

CREATE OR REPLACE FUNCTION fn_calculate_proposal_amount(
    p_product_id INT,
    p_num_users INT
)
RETURNS NUMERIC AS $$
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
$$ LANGUAGE plpgsql;

-- Function: campaign conversion rate
-- HU-05 - endpoint GET /campaigns/{id}/conversion-rate

CREATE OR REPLACE FUNCTION fn_campaign_conversion_rate(
    p_campaign_id INT
)
RETURNS NUMERIC AS $$
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
$$ LANGUAGE plpgsql;

-- verify created objects
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_type, routine_name;

SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table;

-- =====================================================================
-- Session 3 additions - Developer: Jenn Olaya - HU-01, HU-06, HU-07
-- Alert / follow-up automation cycle
-- =====================================================================

-- HT-S3-10  Trigger: mark alert as attended when a follow-up is registered (HU-07)
-- Fires after every INSERT on follow_ups. If the follow-up references an alert,
-- that alert is automatically moved to 'attended'. Connects HU-07 with HU-06.

CREATE OR REPLACE FUNCTION trg_fn_followup_alert()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.alert_id IS NOT NULL THEN
        UPDATE sales_alerts
        SET status = 'attended'
        WHERE alert_id = NEW.alert_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_followup_alert ON follow_ups;
CREATE TRIGGER trg_followup_alert
AFTER INSERT ON follow_ups
FOR EACH ROW
EXECUTE FUNCTION trg_fn_followup_alert();

-- HT-S3-11  Function: escalate overdue alerts (HU-06)
-- Moves every 'pending' alert older than 24 hours to 'escalated'.
-- Returns the number of escalated alerts. Endpoint: POST /alerts/escalate

CREATE OR REPLACE FUNCTION fn_escalate_alerts()
RETURNS INT AS $$
DECLARE
    v_count INT;
BEGIN
    UPDATE sales_alerts
    SET status = 'escalated'
    WHERE status = 'pending'
      AND alert_date < NOW() - INTERVAL '24 hours';

    GET DIAGNOSTICS v_count = ROW_COUNT;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- HT-S3-12  Function: seller management report (HU-01)
-- Summary per seller: total alerts, attended alerts, follow-ups done,
-- managed clients and attention rate. Endpoint: GET /sellers/{id}/report

CREATE OR REPLACE FUNCTION fn_seller_report(p_seller_id INT)
RETURNS TABLE(
    total_alerts BIGINT,
    attended_alerts BIGINT,
    total_followups BIGINT,
    managed_clients BIGINT,
    attention_rate NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM sales_alerts WHERE seller_id = p_seller_id),
        (SELECT COUNT(*) FROM sales_alerts WHERE seller_id = p_seller_id AND status = 'attended'),
        (SELECT COUNT(*) FROM follow_ups  WHERE seller_id = p_seller_id),
        (SELECT COUNT(DISTINCT client_id) FROM follow_ups WHERE seller_id = p_seller_id),
        COALESCE(ROUND(
            (SELECT COUNT(*) FROM sales_alerts WHERE seller_id = p_seller_id AND status = 'attended') * 100.0
            / NULLIF((SELECT COUNT(*) FROM sales_alerts WHERE seller_id = p_seller_id), 0), 2
        ), 0.00);
END;
$$ LANGUAGE plpgsql;

-- HT-S3-11b  UDF: alert response rate per seller (HU-06)
-- Percentage of alerts attended or escalated over the seller's total alerts.
-- Endpoint: GET /sellers/{id}/alert-rate

CREATE OR REPLACE FUNCTION fn_alert_response_rate(p_seller_id INT)
RETURNS DECIMAL AS $$
DECLARE
    v_rate DECIMAL;
BEGIN
    SELECT ROUND(
        COUNT(CASE WHEN status IN ('attended', 'escalated') THEN 1 END) * 100.0
        / NULLIF(COUNT(*), 0), 2
    ) INTO v_rate
    FROM sales_alerts
    WHERE seller_id = p_seller_id;

    RETURN COALESCE(v_rate, 0.00);
END;
$$ LANGUAGE plpgsql;

-- HT-S3-12b  SP: follow-up summary per seller (HU-07)
-- Total follow-ups, clients with a pending next contact, most used contact
-- type and most common result. Endpoint: GET /sellers/{id}/followup-summary

CREATE OR REPLACE FUNCTION fn_followup_summary(p_seller_id INT)
RETURNS TABLE(
    total_followups BIGINT,
    pending_contacts BIGINT,
    most_used_contact_type VARCHAR,
    most_common_result VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*)::BIGINT,
        COUNT(*) FILTER (WHERE next_contact >= CURRENT_DATE)::BIGINT,
        MODE() WITHIN GROUP (ORDER BY contact_type)::VARCHAR,
        MODE() WITHIN GROUP (ORDER BY result)::VARCHAR
    FROM follow_ups
    WHERE seller_id = p_seller_id;
END;
$$ LANGUAGE plpgsql;

-- verify Jenn's objects
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name IN ('fn_escalate_alerts','fn_seller_report','fn_alert_response_rate','fn_followup_summary')
ORDER BY routine_name;

SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public' AND trigger_name = 'trg_followup_alert';
