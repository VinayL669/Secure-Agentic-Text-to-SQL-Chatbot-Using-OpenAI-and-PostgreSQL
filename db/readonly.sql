CREATE ROLE chatbot_readonly LOGIN PASSWORD 'readonly12345';
ALTER ROLE chatbot_readonly SET default_transaction_read_only = on;
ALTER ROLE chatbot_readonly SET statement_timeout = '5s';
GRANT CONNECT ON DATABASE chatbot TO chatbot_readonly;
GRANT USAGE ON SCHEMA public TO chatbot_readonly;
GRANT SELECT ON customers, orders TO chatbot_readonly;