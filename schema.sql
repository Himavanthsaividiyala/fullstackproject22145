-- schema.sql
-- This file defines the structure of the database table.

-- Drop the table if it already exists to start fresh.
DROP TABLE IF EXISTS expenses;

-- Create the expenses table with an added 'payment_method' column
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    payment_method TEXT NOT NULL
);