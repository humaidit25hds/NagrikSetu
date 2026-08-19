-- =========================================
-- CITIZEN AI DATABASE
-- =========================================

-- Users / Citizens
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    age INTEGER,
    state VARCHAR(100),
    income DECIMAL(12, 2),
    is_student BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Government Services / Schemes
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    department VARCHAR(200),
    eligibility TEXT,
    documents_required TEXT,
    application_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Citizen Applications
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,

    status VARCHAR(50) DEFAULT 'pending',

    application_data JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_service
        FOREIGN KEY (service_id)
        REFERENCES services(id)
        ON DELETE CASCADE
);


-- =========================================
-- SAMPLE GOVERNMENT SERVICES
-- =========================================

INSERT INTO services
    (name, description, department, eligibility, documents_required)
VALUES
(
    'Passport Application',
    'Apply for a new passport through the official passport service.',
    'Ministry of External Affairs',
    'Eligibility depends on applicant requirements.',
    'Identity proof, address proof, photographs'
),
(
    'Aadhaar Services',
    'Aadhaar enrolment and update related services.',
    'UIDAI',
    'Available to eligible residents.',
    'Identity and supporting documents'
),
(
    'Government Scholarship',
    'Government scholarship information and application support.',
    'Education Department',
    'Eligibility depends on the specific scholarship scheme.',
    'Income certificate, academic documents, identity proof'
),
(
    'Voter ID Services',
    'Voter registration and voter information update services.',
    'Election Commission of India',
    'Eligible Indian citizens.',
    'Identity proof, address proof'
);


-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX IF NOT EXISTS idx_users_email
ON users(email);

CREATE INDEX IF NOT EXISTS idx_services_name
ON services(name);

CREATE INDEX IF NOT EXISTS idx_applications_user
ON applications(user_id);

CREATE INDEX IF NOT EXISTS idx_applications_service
ON applications(service_id);

CREATE INDEX IF NOT EXISTS idx_applications_status
ON applications(status);{
  "status": "healthy",
  "database": "connected",
  "mongodb": "connected"
}