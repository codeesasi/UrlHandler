CREATE OR REPLACE PROCEDURE stp_users_insert(
    IN input_username VARCHAR,
    IN input_password VARCHAR,
    IN input_email VARCHAR,
    OUT output_userid UUID
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO tbl_Users (Username, Password, Email)
    VALUES (input_username, input_password, input_email)
    RETURNING UserId INTO output_userid;
    
    RAISE NOTICE 'User inserted successfully with ID: %', output_userid;
EXCEPTION 
    WHEN unique_violation THEN
        RAISE EXCEPTION 'Username or email already exists';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error inserting user: %', SQLERRM;
END;
$$;
