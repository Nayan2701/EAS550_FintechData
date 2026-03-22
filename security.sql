
CREATE ROLE analyst_role;
GRANT USAGE ON SCHEMA public TO analyst_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_role;

CREATE ROLE app_user_role;
GRANT USAGE ON SCHEMA public TO app_user_role;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user_role;