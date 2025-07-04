CREATE OR REPLACE FUNCTION fn_insert_url(
    input_url TEXT,
    input_title TEXT DEFAULT NULL,
    input_thumbnail TEXT DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
    generated_uuid UUID := uuid_generate_v4();
    existing_count INT;
BEGIN
    SELECT COUNT(*) INTO existing_count
    FROM tbl_UrlQueue
    WHERE URL = input_url;

    IF existing_count > 0 THEN
        RETURN 'Already processed';
    END IF;

    INSERT INTO tbl_UrlQueue (URLId, URL)
    VALUES (generated_uuid, input_url);

    INSERT INTO tbl_UrlQueue_cache (URLId, Title, Thumbnail)
    VALUES (generated_uuid, input_title, input_thumbnail);

    RETURN 'Inserted successfully';
END;
$$ LANGUAGE plpgsql;
