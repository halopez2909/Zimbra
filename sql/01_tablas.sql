-- Zimbra Transactional System - Session 1
-- Database schema for PostgreSQL
-- Course: Transactional Systems - Uniminuto 2026

CREATE TABLE IF NOT EXISTS sellers (
    seller_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(30),
    active INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS clients (
    client_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    company VARCHAR(150),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(30),
    client_type VARCHAR(50) NOT NULL,
    assigned_seller_id INT REFERENCES sellers(seller_id),
    registration_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150),
    description VARCHAR(250),
    product_type VARCHAR(50) NOT NULL,
    base_price DECIMAL(12,2) NOT NULL,
    max_users INT
);

CREATE TABLE IF NOT EXISTS marketing_campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(200),
    campaign_type VARCHAR(50) NOT NULL,
    objective VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(12,2),
    status VARCHAR(50) NOT NULL,
    tool VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS marketing_interactions (
    interaction_id SERIAL PRIMARY KEY,
    campaign_id INT NOT NULL REFERENCES marketing_campaigns(campaign_id),
    client_id INT NOT NULL REFERENCES clients(client_id),
    interaction_type VARCHAR(50) NOT NULL,
    interaction_date TIMESTAMP DEFAULT NOW(),
    score INT DEFAULT 0,
    converted INT DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_alerts (
    alert_id SERIAL PRIMARY KEY,
    interaction_id INT NOT NULL REFERENCES marketing_interactions(interaction_id),
    seller_id INT NOT NULL REFERENCES sellers(seller_id),
    alert_date TIMESTAMP DEFAULT NOW(),
    alert_type VARCHAR(100),
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS follow_ups (
    followup_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(client_id),
    seller_id INT NOT NULL REFERENCES sellers(seller_id),
    alert_id INT REFERENCES sales_alerts(alert_id),
    contact_type VARCHAR(50) NOT NULL,
    contact_date TIMESTAMP DEFAULT NOW(),
    result VARCHAR(100),
    notes VARCHAR(300),
    next_contact DATE
);

CREATE TABLE IF NOT EXISTS sales_proposals (
    proposal_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(client_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    interaction_id INT REFERENCES marketing_interactions(interaction_id),
    num_users INT NOT NULL,
    proposed_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    estimated_close_date DATE,
    notes VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,
    proposal_id INT NOT NULL UNIQUE REFERENCES sales_proposals(proposal_id),
    client_id INT NOT NULL REFERENCES clients(client_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    final_amount DECIMAL(12,2) NOT NULL,
    num_users INT NOT NULL,
    sale_date TIMESTAMP DEFAULT NOW(),
    payment_method VARCHAR(50),
    origin_channel VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS performance_reports (
    report_id SERIAL PRIMARY KEY,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_visitors INT DEFAULT 0,
    total_downloads INT DEFAULT 0,
    total_prospects INT DEFAULT 0,
    total_proposals INT DEFAULT 0,
    total_sales INT DEFAULT 0,
    total_revenue DECIMAL(14,2) DEFAULT 0,
    conversion_rate_pct DECIMAL(5,2) DEFAULT 0,
    close_rate_pct DECIMAL(5,2) DEFAULT 0,
    generated_at TIMESTAMP DEFAULT NOW()
);
