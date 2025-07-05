CREATE OR REPLACE PROCEDURE stp_users_delete(
    IN input_userid UUID
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Soft delete by setting IsActive to false
    UPDATE tbl_Users
    SET IsActive = FALSE
    WHERE UserId = input_userid;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;
    
    RAISE NOTICE 'User deleted successfully';
EXCEPTION 
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error deleting user: %', SQLERRM;
END;
$$;
