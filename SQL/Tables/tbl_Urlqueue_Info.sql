-- Create the cache table and relate URLId as a foreign key
CREATE TABLE IF NOT EXISTS tbl_UrlQueue_info (
    URLId UUID PRIMARY KEY,
    CreateDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Title TEXT NULL,
    Thumbnail TEXT NULL,
    CONSTRAINT fk_url FOREIGN KEY (URLId) REFERENCES tbl_UrlQueue(URLId) ON DELETE CASCADE
);