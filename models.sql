-- ============================================
-- Legal System Database Schema
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS legal_db;
USE legal_db;

-- Drop tables if they exist (for clean reinstallation)
DROP TABLE IF EXISTS hearings;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS cases;
DROP TABLE IF EXISTS lawyers;
DROP TABLE IF EXISTS clients;

-- Create clients table
CREATE TABLE clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT
);

-- Create Lawyers table
CREATE TABLE lawyers (
    lawyer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100)
);

-- Create cases table
CREATE TABLE cases (
    case_id INT PRIMARY KEY AUTO_INCREMENT,
    case_number VARCHAR(50) UNIQUE NOT NULL,
    case_type VARCHAR(100),
    status ENUM('Active', 'Closed', 'Pending') DEFAULT 'Active',
    client_id INT,
    lawyer_id INT,
    filing_date DATE,
    description TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE SET NULL,
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id) ON DELETE SET NULL
);

-- Create documents table
CREATE TABLE documents (
    doc_id INT PRIMARY KEY AUTO_INCREMENT,
    case_id INT,
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50),
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(500),
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);

-- Create Hearings table
CREATE TABLE hearings (
    hearing_id INT PRIMARY KEY AUTO_INCREMENT,
    case_id INT,
    hearing_date DATETIME,
    notes TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);