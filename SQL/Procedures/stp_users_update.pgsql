CREATE OR REPLACE PROCEDURE stp_users_update(
    IN input_userid UUID,
    IN input_username VARCHAR = NULL,
    IN input_password VARCHAR = NULL,
    IN input_email VARCHAR = NULL,
    IN input_isactive BOOLEAN = NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE tbl_Users
    SET 
        Username = COALESCE(input_username, Username),
        Password = COALESCE(input_password, Password),
        Email = COALESCE(input_email, Email),
        IsActive = COALESCE(input_isactive, IsActive)
    WHERE UserId = input_userid;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;
    
    RAISE NOTICE 'User updated successfully';
EXCEPTION 
    WHEN unique_violation THEN
        RAISE EXCEPTION 'Username or email already exists';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error updating user: %', SQLERRM;
END;
$$;
