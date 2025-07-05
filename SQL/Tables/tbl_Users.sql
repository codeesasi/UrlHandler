CREATE TABLE IF NOT EXISTS tbl_Users (
    UserId UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Username VARCHAR(100) NOT NULL,
    Password VARCHAR(256) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    LastLoginDate TIMESTAMP NULL,
    IsActive BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_users_username UNIQUE (Username),
    CONSTRAINT uq_users_email UNIQUE (Email)
);

-- Add indices for common queries
CREATE INDEX IF NOT EXISTS idx_users_username ON tbl_Users(Username);
CREATE INDEX IF NOT EXISTS idx_users_email ON tbl_Users(Email);
CREATE INDEX IF NOT EXISTS idx_users_createddate ON tbl_Users(CreatedDate);
