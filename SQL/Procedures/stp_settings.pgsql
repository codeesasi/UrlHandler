CREATE OR REPLACE PROCEDURE stp_update_setting(
    IN p_key VARCHAR(50),
    IN p_value TEXT,
    IN p_userid UUID
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO tbl_Settings (SettingKey, SettingValue, UserID, LastModified)
    VALUES (p_key, p_value, p_userid, CURRENT_TIMESTAMP)
    ON CONFLICT (SettingKey, UserID) 
    DO UPDATE SET 
        SettingValue = p_value,
        LastModified = CURRENT_TIMESTAMP;
END;
$$;

CREATE OR REPLACE FUNCTION stp_get_settings(p_userid UUID)
RETURNS TABLE (
    setting_key VARCHAR(50),
    setting_value TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT SettingKey, SettingValue
    FROM tbl_Settings
    WHERE UserID = p_userid;
END;
$$;
