f = open('sql/04_triggers_procedures.sql', 'a', encoding='utf-8')
D = chr(36) + chr(36)
f.write(f"""
-- Trigger 3: update client type to commercial after sale is registered
-- HU-02 Aleja - fires after insert on sales

CREATE OR REPLACE FUNCTION trg_fn_update_client_type()
RETURNS TRIGGER AS {D}
BEGIN
    UPDATE clients
    SET client_type = 'commercial'
    WHERE client_id = NEW.client_id;
    RETURN NEW;
END;
{D} LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_client_type ON sales;
CREATE TRIGGER trg_update_client_type
AFTER INSERT ON sales
FOR EACH ROW
EXECUTE FUNCTION trg_fn_update_client_type();

-- Trigger 4: update campaign status to high_demand when interactions exceed 50
-- HU-04 Aleja - fires after insert on marketing_interactions

CREATE OR REPLACE FUNCTION trg_fn_campaign_demand()
RETURNS TRIGGER AS {D}
DECLARE
    v_count INT;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM marketing_interactions
    WHERE campaign_id = NEW.campaign_id;

    IF v_count > 50 THEN
        UPDATE marketing_campaigns
        SET status = 'high_demand'
        WHERE campaign_id = NEW.campaign_id
        AND status != 'high_demand';
    END IF;
    RETURN NEW;
END;
{D} LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_campaign_demand ON marketing_interactions;
CREATE TRIGGER trg_campaign_demand
AFTER INSERT ON marketing_interactions
FOR EACH ROW
EXECUTE FUNCTION trg_fn_campaign_demand();

-- Function: performance report by period
-- HU-10 Aleja - endpoint GET /reports/performance

CREATE OR REPLACE FUNCTION fn_performance_report(
    p_start DATE,
    p_end DATE
)
RETURNS TABLE(
    period_start DATE,
    period_end DATE,
    total_visitors INT,
    total_downloads INT,
    total_prospects INT,
    total_proposals INT,
    total_sales INT,
    total_revenue NUMERIC,
    conversion_rate_pct NUMERIC,
    close_rate_pct NUMERIC
) AS {D}
BEGIN
    RETURN QUERY
    SELECT
        pr.period_start,
        pr.period_end,
        pr.total_visitors,
        pr.total_downloads,
        pr.total_prospects,
        pr.total_proposals,
        pr.total_sales,
        pr.total_revenue,
        pr.conversion_rate_pct,
        pr.close_rate_pct
    FROM performance_reports pr
    WHERE pr.period_start >= p_start
    AND pr.period_end <= p_end
    ORDER BY pr.period_start;
END;
{D} LANGUAGE plpgsql;

-- Function: campaign stats
-- HU-04 Aleja - endpoint GET /campaigns/{{id}}/stats

CREATE OR REPLACE FUNCTION fn_campaign_stats(
    p_campaign_id INT
)
RETURNS TABLE(
    total_interactions BIGINT,
    total_converted BIGINT,
    conversion_rate NUMERIC,
    cost_per_conversion NUMERIC
) AS {D}
DECLARE
    v_budget NUMERIC;
BEGIN
    SELECT budget INTO v_budget
    FROM marketing_campaigns
    WHERE campaign_id = p_campaign_id;

    RETURN QUERY
    SELECT
        COUNT(*)::BIGINT AS total_interactions,
        SUM(converted)::BIGINT AS total_converted,
        ROUND(SUM(converted) * 100.0 / NULLIF(COUNT(*), 0), 2) AS conversion_rate,
        ROUND(v_budget / NULLIF(SUM(converted), 0), 2) AS cost_per_conversion
    FROM marketing_interactions
    WHERE campaign_id = p_campaign_id;
END;
{D} LANGUAGE plpgsql;
""")
f.close()
print('OK')
