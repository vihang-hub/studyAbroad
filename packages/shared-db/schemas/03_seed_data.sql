-- Seed data for development
-- This script populates the database with initial test data

-- Insert sample countries
INSERT INTO countries (code, name, description) VALUES
('USA', 'United States', 'Leading destination for international students with diverse programs'),
('GBR', 'United Kingdom', 'Historic universities and world-class education system'),
('CAN', 'Canada', 'Welcoming environment with high-quality education'),
('AUS', 'Australia', 'Growing study destination with excellent research facilities'),
('DEU', 'Germany', 'Strong engineering and research programs with low tuition'),
('FRA', 'France', 'Rich cultural experience with renowned institutions'),
('JPN', 'Japan', 'Advanced technology and unique cultural immersion'),
('NLD', 'Netherlands', 'English-taught programs and international environment')
ON CONFLICT (code) DO NOTHING;

-- Insert sample subjects
INSERT INTO subjects (name, category, description) VALUES
('Computer Science', 'STEM', 'Software development, AI, and computational theory'),
('Business Administration', 'Business', 'Management, finance, and entrepreneurship'),
('Engineering', 'STEM', 'Various engineering disciplines'),
('Medicine', 'Health Sciences', 'Medical education and healthcare'),
('Psychology', 'Social Sciences', 'Human behavior and mental processes'),
('Data Science', 'STEM', 'Analytics, machine learning, and big data'),
('International Relations', 'Social Sciences', 'Global politics and diplomacy'),
('Environmental Science', 'Sciences', 'Sustainability and environmental studies')
ON CONFLICT DO NOTHING;

-- Note: Users and chat sessions will be created by the application
-- Documents will be populated by the RAG ingestion process
