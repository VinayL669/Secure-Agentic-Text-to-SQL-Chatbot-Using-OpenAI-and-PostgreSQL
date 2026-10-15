DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    city       TEXT NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (id),
    status      TEXT NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL,
    created_at  DATE NOT NULL
);

INSERT INTO customers (name, city, created_at) VALUES
    ('Asha',  'Hyderabad', '2026-01-10'),
    ('Ravi',  'Mumbai',    '2026-02-05'),
    ('Meera', 'Hyderabad', '2026-02-20'),
    ('Kiran', 'Delhi',     '2026-03-15'),
    ('Sana',  'Mumbai',    '2026-03-28');

INSERT INTO orders (customer_id, status, amount, created_at) VALUES
    (1, 'completed', 500.00,  '2026-02-01'),
    (1, 'completed', 300.00,  '2026-03-05'),
    (1, 'cancelled', 150.00,  '2026-03-06'),
    (2, 'completed', 1200.00, '2026-02-10'),
    (2, 'pending',   400.00,  '2026-03-20'),
    (3, 'completed', 250.00,  '2026-03-01'),
    (3, 'completed', 750.00,  '2026-03-18'),
    (4, 'cancelled', 900.00,  '2026-03-25'),
    (4, 'completed', 100.00,  '2026-04-02'),
    (5, 'completed', 600.00,  '2026-04-05');