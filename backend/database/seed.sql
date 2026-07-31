-- Clear existing data
DELETE FROM schemes;
DELETE FROM sqlite_sequence WHERE name='schemes';
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name='users';

-- Insert Sample Government Schemes
INSERT INTO schemes (
    title, description, category, eligibility_criteria, 
    benefits, deadline, required_documents, application_url, department
) VALUES 
(
    'PM Kisan Samman Nidhi Yojana',
    'An initiative by the Government of India that provides up to ₹6,000 per year in three equal installments to all small and marginal farmers as minimum income support.',
    'Agriculture',
    'Must be a small or marginal farmer who owns cultivable land in India. Available to both male and female farmers. Annual family income threshold is not strictly capped, but institutional landholders, income tax payers, and high-income retired professionals are excluded.',
    'Financial benefit of ₹6,000 per annum, paid in three equal installments of ₹2,000 every four months directly into the bank accounts of farmers.',
    '2026-12-31',
    '["Aadhaar Card", "Income Certificate", "Domicile Certificate", "Other"]',
    'https://pmkisan.gov.in/',
    'Department of Agriculture and Farmers Welfare'
),
(
    'Post Matric Scholarship Scheme for SC Students',
    'A centrally sponsored scheme that provides financial assistance to Scheduled Caste students studying at post-matriculation or post-secondary stages to enable them to complete their education.',
    'Education',
    'Must belong to the Scheduled Caste (SC) category. Must have completed matriculation/secondary education. Annual family income of the parents/guardian from all sources must not exceed ₹2,50,000.',
    'Full tuition fee reimbursement and a monthly maintenance allowance ranging from ₹550 to ₹1,200 depending on the course group.',
    '2026-10-31',
    '["Aadhaar Card", "Caste Certificate", "Income Certificate", "Educational Marksheet", "Domicile Certificate"]',
    'https://scholarships.gov.in/',
    'Ministry of Social Justice and Empowerment'
),
(
    'Pradhan Mantri Awas Yojana (Urban)',
    'A flagship mission of the Government of India that addresses urban housing shortage among the EWS/LIG and MIG categories by ensuring a pucca house to all eligible urban households.',
    'Housing',
    'The beneficiary family should not own a pucca house in their name anywhere in India. Annual family income must be under ₹3,00,000 for Economically Weaker Section (EWS) and under ₹6,00,000 for Low Income Group (LIG).',
    'Interest subsidy of up to 6.5% on home loans up to a tenure of 20 years, saving beneficiaries up to ₹2.67 Lakhs in loan repayments.',
    '2026-09-30',
    '["Aadhaar Card", "Income Certificate", "Domicile Certificate", "PAN Card"]',
    'https://pmay-urban.gov.in/',
    'Ministry of Housing and Urban Affairs'
),
(
    'Pradhan Mantri MUDRA Yojana (PMMY)',
    'A scheme to provide loans up to ₹10 Lakhs to non-corporate, non-farm small/micro enterprises. These loans are classified as Shishu (up to ₹50k), Kishor (up to ₹5 Lakhs), and Tarun (up to ₹10 Lakhs).',
    'Business',
    'Any Indian citizen who has a business plan for a non-farm sector income-generating activity such as manufacturing, processing, trading, or service sector, and whose loan requirement is less than ₹10 Lakhs.',
    'Collateral-free business loans up to ₹10,00,000 with flexible interest rates and repayment periods up to 5 years.',
    NULL,
    '["Aadhaar Card", "PAN Card", "Domicile Certificate", "Other"]',
    'https://www.mudra.org.in/',
    'Department of Financial Services'
),
(
    'Ayushman Bharat National Health Protection Scheme',
    'A national public health insurance scheme that aims to provide free access to health insurance coverage for low-income families in the country.',
    'Healthcare',
    'Identified households based on deprivation and occupational criteria in the Socio-Economic Caste Census (SECC) database for rural and urban areas. No cap on family size or age.',
    'Cashless health cover of up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization.',
    NULL,
    '["Aadhaar Card", "Other"]',
    'https://pmjay.gov.in/',
    'Ministry of Health and Family Welfare'
),
(
    'Lakhpati Didi Skill Development Scheme',
    'A program to empower rural women by providing them with skill training in entrepreneurship, agriculture, and tech tasks (such as drone operation, plumbing, tailoring) to enable them to earn at least ₹1,00,000 per year.',
    'Women Empowerment',
    'Must be an Indian woman, resident of a rural area, and preferably a member of a Self-Help Group (SHG). Age group of 18 to 50 years.',
    'Free skill training, financial literacy workshops, and low-interest loan options to scale and build sustainable self-employment ventures.',
    '2026-11-30',
    '["Aadhaar Card", "Domicile Certificate", "Income Certificate"]',
    'https://lakhpatididi.gov.in/',
    'Ministry of Rural Development'
);

-- Insert Sample Users with pre-hashed passwords ('password123')
INSERT INTO users (
    full_name, email, password_hash, phone_number, age, gender,
    state, district, education, occupation, annual_family_income,
    category, is_disabled
) VALUES 
(
    'Ramesh Kurian',
    'ramesh.kurian@example.com',
    'scrypt:32768:8:1$3cDq7uttXjgNfUIw$a333dc782667a3c77ecc8c1f09ce78205264df592af1167856cfdd715b843f846400aad74b6149831f0206902db4f2c4e041156b323146d71dbcb31d41a7c324',
    '9876543210',
    45,
    'Male',
    'Kerala',
    'Ernakulam',
    'High School',
    'Farmer',
    85000.0,
    'General',
    0
),
(
    'Ananya Sharma',
    'ananya.sharma@example.com',
    'scrypt:32768:8:1$3cDq7uttXjgNfUIw$a333dc782667a3c77ecc8c1f09ce78205264df592af1167856cfdd715b843f846400aad74b6149831f0206902db4f2c4e041156b323146d71dbcb31d41a7c324',
    '9123456789',
    20,
    'Female',
    'Kerala',
    'Trivandrum',
    'Undergraduate (B.Tech)',
    'Student',
    180000.0,
    'SC',
    0
),
(
    'Pooja Deshmukh',
    'pooja.d@example.com',
    'scrypt:32768:8:1$3cDq7uttXjgNfUIw$a333dc782667a3c77ecc8c1f09ce78205264df592af1167856cfdd715b843f846400aad74b6149831f0206902db4f2c4e041156b323146d71dbcb31d41a7c324',
    '8123456780',
    28,
    'Female',
    'Maharashtra',
    'Pune',
    'Postgraduate',
    'Unemployed',
    45000.0,
    'EWS',
    1
);
