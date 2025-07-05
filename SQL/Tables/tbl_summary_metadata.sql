CREATE TABLE IF NOT EXISTS tbl_summary_metadata (
    URLID UUID PRIMARY KEY,
    CreateDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    URL TEXT NOT NULL CHECK (length(URL) <= 2048),
    RawText TEXT NULL CHECK (length(RawText) <= 10000),
    Summary TEXT NULL CHECK (length(Summary) <= 5000),
    Keywords TEXT NULL CHECK (length(Keywords) <= 1000),
    Tone TEXT NULL CHECK (length(Tone) <= 50),
    Rating INT DEFAULT 0 CHECK (Rating BETWEEN 0 AND 5),
    Model VARCHAR(100) NULL,
    CONSTRAINT uq_summary_url UNIQUE (URL),
    CONSTRAINT fk_summary_url FOREIGN KEY (URLID) 
        REFERENCES tbl_UrlQueue(URLId) ON DELETE CASCADE
);

-- Add indices for common queries
CREATE INDEX IF NOT EXISTS idx_summary_createdate ON tbl_summary_metadata(CreateDate);
CREATE INDEX IF NOT EXISTS idx_summary_url ON tbl_summary_metadata(URL);
CREATE INDEX IF NOT EXISTS idx_summary_rating ON tbl_summary_metadata(Rating);