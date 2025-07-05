CREATE OR REPLACE PROCEDURE stp_user_login(
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(256),
    OUT out_success BOOLEAN,
    OUT out_email VARCHAR(255),
    OUT out_role VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT TRUE, Email, 'user' INTO out_success, out_email, out_role
    FROM tbl_Users
    WHERE Email = p_email 
    AND Password = p_password
    AND IsActive = TRUE;

    IF out_success THEN
        UPDATE tbl_Users 
        SET LastLoginDate = CURRENT_TIMESTAMP 
        WHERE Email = p_email;
    END IF;

    IF out_success IS NULL THEN
        out_success := FALSE;
    END IF;
END;
$$;
