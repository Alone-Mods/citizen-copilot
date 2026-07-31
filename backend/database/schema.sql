PRAGMA foreign_keys =ON;
--users
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    phone_number TEXT,
    age INTEGER CHECK (age >= 0 AND age <= 120),
    gender TEXT CHECK (gender IN ('Male','Female','Non-Binary','Other','Prefer Not to Say')),
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    education TEXT,
    occupation TEXT,
    annual_family_income REAL CHECK (annual_family_income >= 0),
    category TEXT CHECK (category IN ('General','OBC','SC','ST','EWS')),
    is_disabled INTEGER NOT NULL DEFAULT 0 CHECK (is_disabled IN (0,1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--schemes
CREATE TABLE schemes (
    scheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL CHECK (
        category IN (
            'Education',
            'Healthcare',
            'Agriculture',
            'Employment',
            'Women Empowerment',
            'Business',
            'Housing',
            'Social Welfare',
            'Skill Development',
            'Other'
        )
    ),
    eligibility_criteria TEXT NOT NULL,
    benefits TEXT NOT NULL,
    deadline DATE,
    required_documents TEXT,
    application_url TEXT NOT NULL,
    department TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--doc

CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_type TEXT NOT NULL CHECK (
        document_type IN (
            'Aadhaar Card',
            'PAN Card',
            'Income Certificate',
            'Caste Certificate',
            'Disability Certificate',
            'Educational Marksheet',
            'Domicile Certificate',
            'Other'
        )
    ),
    original_filename TEXT NOT NULL,
    stored_file_path TEXT NOT NULL UNIQUE,
    upload_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verification_status TEXT NOT NULL DEFAULT 'Pending' CHECK (
        verification_status IN ('Pending', 'Verified', 'Rejected')
    ),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

--notification


CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_type TEXT NOT NULL CHECK (
        notification_type IN (
            'Scheme Match',
            'Deadline Reminder',
            'Document Verification',
            'System Alert',
            'General'
        )
    ),
    is_read INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

--eligibility


CREATE TABLE eligibility_history (
history_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
scheme_id INTEGER NOT NULL,
eligibility_result TEXT NOT NULL CHECK (
eligibility_result IN ('Eligible', 'Ineligible', 'Conditionally Eligible')
),
match_percentage REAL NOT NULL CHECK (
match_percentage >= 0.0 AND match_percentage <= 100.0
),
ai_explanation TEXT NOT NULL,
missing_requirements TEXT,
checked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (scheme_id) REFERENCES schemes (scheme_id) ON DELETE CASCADE ON UPDATE CASCADE
);