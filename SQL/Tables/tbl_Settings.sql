CREATE TABLE IF NOT EXISTS tbl_Settings (
    SettingKey VARCHAR(50),
    UserID UUID NOT NULL,
    SettingValue TEXT NOT NULL,
    LastModified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Description TEXT NULL,
    PRIMARY KEY (SettingKey, UserID),
    FOREIGN KEY (UserID) REFERENCES tbl_Users(UserId) ON DELETE CASCADE
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_settings_userid ON tbl_Settings(UserID);

-- Insert default settings
INSERT INTO tbl_Settings (SettingKey, UserID, SettingValue, Description)
VALUES 
    ('itemsPerPage', '10', 'Number of items to display per page'),
    ('theme', 'light', 'UI theme (light/dark)'),
    ('aiProvider', 'openai', 'AI provider for summarization')
ON CONFLICT (SettingKey) DO NOTHING;
