-- Zimbra Transactional System - Session 2
-- Simulated data - minimum 30 records per table
-- Course: Transactional Systems - Uniminuto 2026

-- sellers (10)
INSERT INTO sellers (full_name, email, phone, active) VALUES
('Carlos Mendez', 'cmendez@zimbra.com', '3001234501', 1),
('Laura Ospina', 'lospina@zimbra.com', '3001234502', 1),
('Diego Herrera', 'dherrera@zimbra.com', '3001234503', 1),
('Sofia Vargas', 'svargas@zimbra.com', '3001234504', 1),
('Andres Torres', 'atorres@zimbra.com', '3001234505', 1),
('Maria Pinto', 'mpinto@zimbra.com', '3001234506', 1),
('Juan Rios', 'jrios@zimbra.com', '3001234507', 1),
('Camila Reyes', 'creyes@zimbra.com', '3001234508', 1),
('Felipe Arango', 'farango@zimbra.com', '3001234509', 1),
('Isabel Cruz', 'icruz@zimbra.com', '3001234510', 1);

-- clients (35)
INSERT INTO clients (full_name, company, email, phone, client_type, assigned_seller_id) VALUES
('Ana Ruiz', 'TechSol S.A.', 'aruiz@techsol.com', '3101111001', 'prospect', 1),
('Pedro Salcedo', 'GlobalComm', 'psalcedo@globalcomm.com', '3101111002', 'trial', 2),
('Roberto Vega', 'Innovatech', 'rvega@innovatech.com', '3101111003', 'commercial', 1),
('Luisa Mora', 'DataPro', 'lmora@datapro.com', '3101111004', 'trial', 3),
('Jorge Cano', 'NetSystems', 'jcano@netsystems.com', '3101111005', 'prospect', 2),
('Patricia Leon', 'CloudBase', 'pleon@cloudbase.com', '3101111006', 'commercial', 4),
('Ricardo Mejia', 'SoftWave', 'rmejia@softwave.com', '3101111007', 'trial', 1),
('Claudia Suarez', 'AppZone', 'csuarez@appzone.com', '3101111008', 'prospect', 5),
('Hector Perez', 'DataLink', 'hperez@datalink.com', '3101111009', 'trial', 2),
('Natalia Rojas', 'WebTech', 'nrojas@webtech.com', '3101111010', 'commercial', 3),
('Sergio Blanco', 'CoreSoft', 'sblanco@coresoft.com', '3101111011', 'prospect', 1),
('Monica Diaz', 'InfoNet', 'mdiaz@infonet.com', '3101111012', 'trial', 6),
('Andres Garzon', 'TechPrime', 'agarzon@techprime.com', '3101111013', 'commercial', 2),
('Carolina Pena', 'SysPro', 'cpena@syspro.com', '3101111014', 'prospect', 7),
('Mauricio Lara', 'NetCore', 'mlara@netcore.com', '3101111015', 'trial', 1),
('Adriana Castro', 'DevBase', 'acastro@devbase.com', '3101111016', 'commercial', 4),
('Gustavo Mora', 'TechFlow', 'gmora@techflow.com', '3101111017', 'prospect', 3),
('Liliana Vargas', 'CloudPro', 'lvargas@cloudpro.com', '3101111018', 'trial', 5),
('Camilo Restrepo', 'DataSoft', 'crestrepo@datasoft.com', '3101111019', 'commercial', 2),
('Sandra Rios', 'NetWave', 'srios@netwave.com', '3101111020', 'prospect', 1),
('Oscar Mendez', 'AppCore', 'omendez@appcore.com', '3101111021', 'trial', 6),
('Viviana Torres', 'SoftBase', 'vtorres@softbase.com', '3101111022', 'commercial', 3),
('Daniel Herrera', 'InfoPro', 'dherrera@infopro.com', '3101111023', 'prospect', 7),
('Alejandra Gomez', 'WebPrime', 'agomez@webprime.com', '3101111024', 'trial', 1),
('Fernando Ruiz', 'TechNet', 'fruiz@technet.com', '3101111025', 'commercial', 2),
('Paola Jimenez', 'CoreNet', 'pjimenez@corenet.com', '3101111026', 'prospect', 4),
('Nicolas Ospina', 'SysWave', 'nospina@syswave.com', '3101111027', 'trial', 1),
('Valentina Cruz', 'DataZone', 'vcruz@datazone.com', '3101111028', 'commercial', 5),
('Cristian Lopez', 'AppSoft', 'clopez@appsoft.com', '3101111029', 'prospect', 3),
('Marcela Pardo', 'NetPrime', 'mpardo@netprime.com', '3101111030', 'trial', 2),
('Julian Soto', 'TechZone', 'jsoto@techzone.com', '3101111031', 'commercial', 1),
('Bibiana Mora', 'CloudNet', 'bmora@cloudnet.com', '3101111032', 'prospect', 6),
('Esteban Vega', 'SoftPrime', 'evega@softprime.com', '3101111033', 'trial', 4),
('Tatiana Leon', 'InfoZone', 'tleon@infozone.com', '3101111034', 'commercial', 2),
('Rodrigo Pinto', 'WebCore', 'rpinto@webcore.com', '3101111035', 'prospect', 7);

-- products (10) - HU-03 Andres
INSERT INTO products (product_name, description, product_type, base_price, max_users) VALUES
('ZCS Community Edition', 'Free open source version', 'free', 0.00, NULL),
('ZCS Professional 25', 'Up to 25 users, email and collaboration', 'commercial', 1200.00, 25),
('ZCS Professional 50', 'Up to 50 users, full features', 'commercial', 2200.00, 50),
('ZCS Enterprise 100', 'Up to 100 users, advanced features', 'commercial', 4500.00, 100),
('ZCS Enterprise 250', 'Up to 250 users, priority support', 'commercial', 9500.00, 250),
('ZCS Network Edition', 'Unlimited users, 24/7 support', 'commercial', 18000.00, NULL),
('ZCS Cloud Starter', 'Cloud hosted, up to 10 users', 'commercial', 600.00, 10),
('ZCS Cloud Business', 'Cloud hosted, up to 75 users', 'commercial', 3500.00, 75),
('ZCS Cloud Enterprise', 'Cloud hosted, unlimited users', 'commercial', 12000.00, NULL),
('ZCS Education', 'Special pricing for universities', 'commercial', 800.00, 500);

-- marketing_campaigns (10)
INSERT INTO marketing_campaigns (campaign_name, campaign_type, objective, start_date, end_date, budget, status, tool) VALUES
('Q1 Email Campaign', 'email', 'acquisition', '2026-01-01', '2026-03-31', 5000.00, 'finished', 'OneView'),
('Web Tracking Trial Users', 'web_tracking', 'acquisition', '2026-01-01', NULL, 0.00, 'active', 'OneView'),
('SaaS Lead Generation Q1', 'lead_generation', 'acquisition', '2026-02-01', '2026-04-30', 8000.00, 'active', 'OneView'),
('ZCS Pro Web Analysis', 'web', 'acquisition', '2026-03-01', '2026-06-30', 3000.00, 'active', 'OneView'),
('Enterprise Upselling Q1', 'email', 'upselling', '2026-01-15', '2026-03-15', 4000.00, 'finished', 'OneView'),
('Trial Conversion Campaign', 'email', 'retention', '2026-02-01', '2026-04-01', 6000.00, 'active', 'OneView'),
('Cloud Migration Promo', 'lead_generation', 'acquisition', '2026-03-01', '2026-05-31', 7000.00, 'active', 'OneView'),
('Education Sector Outreach', 'email', 'acquisition', '2026-01-01', '2026-06-30', 2500.00, 'active', 'OneView'),
('Reactivation Lost Clients', 'email', 'reactivation', '2026-02-15', '2026-04-15', 3500.00, 'active', 'OneView'),
('Q2 Web Tracking', 'web_tracking', 'acquisition', '2026-04-01', NULL, 0.00, 'active', 'OneView');

-- marketing_interactions (35) - HU-05 Andres
INSERT INTO marketing_interactions (campaign_id, client_id, interaction_type, score, converted) VALUES
(1, 1, 'email_open', 20, 0),
(2, 2, 'trial_download', 60, 0),
(3, 3, 'form_submission', 85, 1),
(1, 4, 'trial_download', 55, 0),
(2, 5, 'web_visit', 15, 0),
(3, 6, 'form_submission', 90, 1),
(4, 7, 'web_visit', 40, 0),
(5, 8, 'email_open', 25, 0),
(6, 9, 'trial_download', 65, 0),
(3, 10, 'form_submission', 88, 1),
(1, 11, 'email_open', 10, 0),
(2, 12, 'trial_download', 70, 0),
(7, 13, 'form_submission', 92, 1),
(4, 14, 'web_visit', 30, 0),
(6, 15, 'trial_download', 75, 0),
(3, 16, 'form_submission', 95, 1),
(1, 17, 'email_open', 20, 0),
(8, 18, 'web_visit', 45, 0),
(9, 19, 'form_submission', 80, 1),
(2, 20, 'web_visit', 10, 0),
(5, 21, 'email_open', 35, 0),
(6, 22, 'form_submission', 82, 1),
(7, 23, 'web_visit', 25, 0),
(3, 24, 'trial_download', 60, 0),
(8, 25, 'form_submission', 87, 1),
(1, 26, 'email_open', 15, 0),
(9, 27, 'trial_download', 55, 0),
(4, 28, 'form_submission', 91, 1),
(2, 29, 'web_visit', 20, 0),
(6, 30, 'email_open', 30, 0),
(7, 31, 'form_submission', 83, 1),
(3, 32, 'web_visit', 10, 0),
(8, 33, 'trial_download', 50, 0),
(5, 34, 'form_submission', 86, 1),
(9, 35, 'web_visit', 15, 0);

-- sales_alerts (15)
INSERT INTO sales_alerts (interaction_id, seller_id, alert_type, status) VALUES
(3, 1, 'high_lead_score', 'attended'),
(6, 4, 'high_lead_score', 'attended'),
(10, 3, 'high_lead_score', 'attended'),
(13, 2, 'high_lead_score', 'attended'),
(16, 4, 'high_lead_score', 'attended'),
(19, 1, 'high_lead_score', 'attended'),
(22, 3, 'high_lead_score', 'attended'),
(25, 2, 'high_lead_score', 'pending'),
(28, 5, 'high_lead_score', 'pending'),
(31, 1, 'high_lead_score', 'pending'),
(34, 2, 'high_lead_score', 'pending'),
(4, 3, 'pending_followup', 'pending'),
(9, 1, 'pending_followup', 'pending'),
(15, 4, 'pending_followup', 'pending'),
(24, 2, 'pending_followup', 'pending');

-- follow_ups (15)
INSERT INTO follow_ups (client_id, seller_id, alert_id, contact_type, result, notes, next_contact) VALUES
(3, 1, 1, 'call', 'interested', 'Client very interested in ZCS Enterprise', '2026-04-15'),
(6, 4, 2, 'email', 'proposal_sent', 'ZCS Network Edition proposal sent', '2026-04-20'),
(10, 3, 3, 'visit', 'negotiation', 'In-person meeting scheduled', '2026-04-18'),
(13, 2, 4, 'call', 'proposal_sent', 'Client requested detailed quote', '2026-04-22'),
(16, 4, 5, 'email', 'interested', 'Client responded positively', '2026-04-16'),
(19, 1, 6, 'call', 'negotiation', 'Discussing contract terms', '2026-04-25'),
(22, 3, 7, 'visit', 'proposal_sent', 'Product demo completed', '2026-04-19'),
(3, 1, NULL, 'call', 'follow_up', 'Post-demo follow up call', '2026-04-30'),
(6, 4, NULL, 'email', 'follow_up', 'Success stories sent', '2026-05-01'),
(10, 3, NULL, 'call', 'interested', 'Confirmed interest in proceeding', '2026-05-02'),
(13, 2, NULL, 'visit', 'negotiation', 'Second negotiation meeting', '2026-05-05'),
(16, 4, NULL, 'email', 'proposal_sent', 'Final proposal sent', '2026-05-03'),
(19, 1, NULL, 'call', 'negotiation', 'Contract clause review', '2026-05-06'),
(22, 3, NULL, 'visit', 'interested', 'Presentation to tech team', '2026-05-07'),
(25, 2, 8, 'email', 'follow_up', 'First contact after alert', '2026-05-08');

-- sales_proposals (15) - HU-08 Andres
INSERT INTO sales_proposals (client_id, product_id, interaction_id, num_users, proposed_amount, status, estimated_close_date, notes) VALUES
(3, 4, 3, 80, 4500.00, 'accepted', '2026-04-15', 'Client requested ZCS Enterprise 100'),
(6, 6, 6, 50, 18000.00, 'accepted', '2026-04-20', 'Full Network Edition for GlobalComm'),
(10, 5, 10, 200, 9500.00, 'accepted', '2026-04-18', 'ZCS Enterprise 250 for WebTech'),
(13, 4, 13, 90, 4500.00, 'sent', '2026-04-22', 'Pending client approval'),
(16, 6, 16, 100, 18000.00, 'negotiation', '2026-04-30', 'Negotiating payment terms'),
(19, 5, 19, 220, 9500.00, 'accepted', '2026-04-25', 'ZCS Enterprise for DataSoft'),
(22, 4, 22, 85, 4500.00, 'sent', '2026-04-30', 'Awaiting signature'),
(25, 3, 25, 45, 2200.00, 'draft', '2026-05-10', 'Initial proposal draft'),
(28, 2, 28, 20, 1200.00, 'negotiation', '2026-05-05', 'Small team package'),
(31, 7, 31, 8, 600.00, 'sent', '2026-05-08', 'Cloud Starter for TechZone'),
(34, 8, 34, 60, 3500.00, 'accepted', '2026-05-03', 'Cloud Business for InfoZone'),
(1, 2, 1, 15, 1200.00, 'draft', '2026-05-15', 'First contact proposal'),
(5, 1, 5, 1, 0.00, 'draft', '2026-05-20', 'Starting with free edition'),
(9, 3, 9, 40, 2200.00, 'rejected', '2026-04-30', 'Client chose competitor'),
(15, 7, 15, 7, 600.00, 'negotiation', '2026-05-12', 'Cloud starter negotiation');

-- sales (5) - HU-09 Andres
INSERT INTO sales (proposal_id, client_id, product_id, final_amount, num_users, payment_method, origin_channel) VALUES
(1, 3, 4, 4500.00, 80, 'wire_transfer', 'email'),
(2, 6, 6, 17500.00, 50, 'wire_transfer', 'web'),
(3, 10, 5, 9500.00, 200, 'credit_card', 'email'),
(6, 19, 5, 9000.00, 220, 'wire_transfer', 'phone'),
(11, 34, 8, 3500.00, 60, 'credit_card', 'web');

-- performance_reports (5)
INSERT INTO performance_reports (period_start, period_end, total_visitors, total_downloads, total_prospects, total_proposals, total_sales, total_revenue, conversion_rate_pct, close_rate_pct) VALUES
('2026-01-01', '2026-01-31', 850000, 42000, 120, 8, 3, 31500.00, 4.94, 37.50),
('2026-02-01', '2026-02-28', 920000, 48000, 145, 10, 4, 38200.00, 5.22, 40.00),
('2026-03-01', '2026-03-31', 1050000, 55000, 180, 12, 5, 44700.00, 5.24, 41.67),
('2026-04-01', '2026-04-30', 980000, 51000, 165, 11, 4, 39500.00, 5.20, 36.36),
('2026-01-01', '2026-03-31', 2820000, 145000, 445, 30, 12, 114400.00, 5.14, 40.00);

-- marketing_campaigns (10)
INSERT INTO marketing_campaigns (campaign_name, campaign_type, objective, start_date, end_date, budget, status, tool) VALUES
('Q1 Email Campaign', 'email', 'acquisition', '2026-01-01', '2026-03-31', 5000.00, 'finished', 'OneView'),
('Web Tracking Trial Users', 'web_tracking', 'acquisition', '2026-01-01', NULL, 0.00, 'active', 'OneView'),
('SaaS Lead Generation Q1', 'lead_generation', 'acquisition', '2026-02-01', '2026-04-30', 8000.00, 'active', 'OneView'),
('ZCS Pro Web Analysis', 'web', 'acquisition', '2026-03-01', '2026-06-30', 3000.00, 'active', 'OneView'),
('Enterprise Upselling Q1', 'email', 'upselling', '2026-01-15', '2026-03-15', 4000.00, 'finished', 'OneView'),
('Trial Conversion Campaign', 'email', 'retention', '2026-02-01', '2026-04-01', 6000.00, 'active', 'OneView'),
('Cloud Migration Promo', 'lead_generation', 'acquisition', '2026-03-01', '2026-05-31', 7000.00, 'active', 'OneView'),
('Education Sector Outreach', 'email', 'acquisition', '2026-01-01', '2026-06-30', 2500.00, 'active', 'OneView'),
('Reactivation Lost Clients', 'email', 'reactivation', '2026-02-15', '2026-04-15', 3500.00, 'active', 'OneView'),
('Q2 Web Tracking', 'web_tracking', 'acquisition', '2026-04-01', NULL, 0.00, 'active', 'OneView');

-- marketing_interactions (35) - HU-05 Andres
INSERT INTO marketing_interactions (campaign_id, client_id, interaction_type, score, converted) VALUES
(1, 1, 'email_open', 20, 0),
(2, 2, 'trial_download', 60, 0),
(3, 3, 'form_submission', 85, 1),
(1, 4, 'trial_download', 55, 0),
(2, 5, 'web_visit', 15, 0),
(3, 6, 'form_submission', 90, 1),
(4, 7, 'web_visit', 40, 0),
(5, 8, 'email_open', 25, 0),
(6, 9, 'trial_download', 65, 0),
(3, 10, 'form_submission', 88, 1),
(1, 11, 'email_open', 10, 0),
(2, 12, 'trial_download', 70, 0),
(7, 13, 'form_submission', 92, 1),
(4, 14, 'web_visit', 30, 0),
(6, 15, 'trial_download', 75, 0),
(3, 16, 'form_submission', 95, 1),
(1, 17, 'email_open', 20, 0),
(8, 18, 'web_visit', 45, 0),
(9, 19, 'form_submission', 80, 1),
(2, 20, 'web_visit', 10, 0),
(5, 21, 'email_open', 35, 0),
(6, 22, 'form_submission', 82, 1),
(7, 23, 'web_visit', 25, 0),
(3, 24, 'trial_download', 60, 0),
(8, 25, 'form_submission', 87, 1),
(1, 26, 'email_open', 15, 0),
(9, 27, 'trial_download', 55, 0),
(4, 28, 'form_submission', 91, 1),
(2, 29, 'web_visit', 20, 0),
(6, 30, 'email_open', 30, 0),
(7, 31, 'form_submission', 83, 1),
(3, 32, 'web_visit', 10, 0),
(8, 33, 'trial_download', 50, 0),
(5, 34, 'form_submission', 86, 1),
(9, 35, 'web_visit', 15, 0);

-- sales_alerts (15)
INSERT INTO sales_alerts (interaction_id, seller_id, alert_type, status) VALUES
(3, 1, 'high_lead_score', 'attended'),
(6, 4, 'high_lead_score', 'attended'),
(10, 3, 'high_lead_score', 'attended'),
(13, 2, 'high_lead_score', 'attended'),
(16, 4, 'high_lead_score', 'attended'),
(19, 1, 'high_lead_score', 'attended'),
(22, 3, 'high_lead_score', 'attended'),
(25, 2, 'high_lead_score', 'pending'),
(28, 5, 'high_lead_score', 'pending'),
(31, 1, 'high_lead_score', 'pending'),
(34, 2, 'high_lead_score', 'pending'),
(4, 3, 'pending_followup', 'pending'),
(9, 1, 'pending_followup', 'pending'),
(15, 4, 'pending_followup', 'pending'),
(24, 2, 'pending_followup', 'pending');

-- follow_ups (15)
INSERT INTO follow_ups (client_id, seller_id, alert_id, contact_type, result, notes, next_contact) VALUES
(3, 1, 1, 'call', 'interested', 'Client very interested in ZCS Enterprise', '2026-04-15'),
(6, 4, 2, 'email', 'proposal_sent', 'ZCS Network Edition proposal sent', '2026-04-20'),
(10, 3, 3, 'visit', 'negotiation', 'In-person meeting scheduled', '2026-04-18'),
(13, 2, 4, 'call', 'proposal_sent', 'Client requested detailed quote', '2026-04-22'),
(16, 4, 5, 'email', 'interested', 'Client responded positively', '2026-04-16'),
(19, 1, 6, 'call', 'negotiation', 'Discussing contract terms', '2026-04-25'),
(22, 3, 7, 'visit', 'proposal_sent', 'Product demo completed', '2026-04-19'),
(3, 1, NULL, 'call', 'follow_up', 'Post-demo follow up call', '2026-04-30'),
(6, 4, NULL, 'email', 'follow_up', 'Success stories sent', '2026-05-01'),
(10, 3, NULL, 'call', 'interested', 'Confirmed interest in proceeding', '2026-05-02'),
(13, 2, NULL, 'visit', 'negotiation', 'Second negotiation meeting', '2026-05-05'),
(16, 4, NULL, 'email', 'proposal_sent', 'Final proposal sent', '2026-05-03'),
(19, 1, NULL, 'call', 'negotiation', 'Contract clause review', '2026-05-06'),
(22, 3, NULL, 'visit', 'interested', 'Presentation to tech team', '2026-05-07'),
(25, 2, 8, 'email', 'follow_up', 'First contact after alert', '2026-05-08');

-- sales_proposals (15) - HU-08 Andres
INSERT INTO sales_proposals (client_id, product_id, interaction_id, num_users, proposed_amount, status, estimated_close_date, notes) VALUES
(3, 4, 3, 80, 4500.00, 'accepted', '2026-04-15', 'Client requested ZCS Enterprise 100'),
(6, 6, 6, 50, 18000.00, 'accepted', '2026-04-20', 'Full Network Edition for GlobalComm'),
(10, 5, 10, 200, 9500.00, 'accepted', '2026-04-18', 'ZCS Enterprise 250 for WebTech'),
(13, 4, 13, 90, 4500.00, 'sent', '2026-04-22', 'Pending client approval'),
(16, 6, 16, 100, 18000.00, 'negotiation', '2026-04-30', 'Negotiating payment terms'),
(19, 5, 19, 220, 9500.00, 'accepted', '2026-04-25', 'ZCS Enterprise for DataSoft'),
(22, 4, 22, 85, 4500.00, 'sent', '2026-04-30', 'Awaiting signature'),
(25, 3, 25, 45, 2200.00, 'draft', '2026-05-10', 'Initial proposal draft'),
(28, 2, 28, 20, 1200.00, 'negotiation', '2026-05-05', 'Small team package'),
(31, 7, 31, 8, 600.00, 'sent', '2026-05-08', 'Cloud Starter for TechZone'),
(34, 8, 34, 60, 3500.00, 'accepted', '2026-05-03', 'Cloud Business for InfoZone'),
(1, 2, 1, 15, 1200.00, 'draft', '2026-05-15', 'First contact proposal'),
(5, 1, 5, 1, 0.00, 'draft', '2026-05-20', 'Starting with free edition'),
(9, 3, 9, 40, 2200.00, 'rejected', '2026-04-30', 'Client chose competitor'),
(15, 7, 15, 7, 600.00, 'negotiation', '2026-05-12', 'Cloud starter negotiation');

-- sales (5) - HU-09 Andres
INSERT INTO sales (proposal_id, client_id, product_id, final_amount, num_users, payment_method, origin_channel) VALUES
(1, 3, 4, 4500.00, 80, 'wire_transfer', 'email'),
(2, 6, 6, 17500.00, 50, 'wire_transfer', 'web'),
(3, 10, 5, 9500.00, 200, 'credit_card', 'email'),
(6, 19, 5, 9000.00, 220, 'wire_transfer', 'phone'),
(11, 34, 8, 3500.00, 60, 'credit_card', 'web');

-- performance_reports (5)
INSERT INTO performance_reports (period_start, period_end, total_visitors, total_downloads, total_prospects, total_proposals, total_sales, total_revenue, conversion_rate_pct, close_rate_pct) VALUES
('2026-01-01', '2026-01-31', 850000, 42000, 120, 8, 3, 31500.00, 4.94, 37.50),
('2026-02-01', '2026-02-28', 920000, 48000, 145, 10, 4, 38200.00, 5.22, 40.00),
('2026-03-01', '2026-03-31', 1050000, 55000, 180, 12, 5, 44700.00, 5.24, 41.67),
('2026-04-01', '2026-04-30', 980000, 51000, 165, 11, 4, 39500.00, 5.20, 36.36),
('2026-01-01', '2026-03-31', 2820000, 145000, 445, 30, 12, 114400.00, 5.14, 40.00);
