CREATE OR REPLACE PROCEDURE stp_insert_summary(
    IN input_urlid UUID,
    IN input_url TEXT,
    IN input_raw_text TEXT,
    IN input_summary TEXT,
    IN input_keywords TEXT DEFAULT NULL,
    IN input_tone TEXT DEFAULT NULL,
    IN input_rating INT DEFAULT 0,
    IN input_model TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    existing_uuid UUID;
BEGIN
    -- Start transaction
    BEGIN
        -- Check if URL already exists
        SELECT URLID INTO existing_uuid
        FROM tbl_summary_metadata
        WHERE URL = input_url;

        IF existing_uuid IS NOT NULL THEN
            RAISE NOTICE 'Summary already exists for URL';
            RETURN;
        END IF;

        -- Insert new summary with provided UUID
        INSERT INTO tbl_summary_metadata (
            URLID,
            URL,
            RawText,
            Summary,
            Keywords,
            Tone,
            Rating,
            Model
        ) VALUES (
            input_urlid,
            input_url,
            input_raw_text,
            input_summary,
            input_keywords,
            input_tone,
            LEAST(GREATEST(input_rating, 0), 5),
            input_model
        );

        RAISE NOTICE 'Summary inserted successfully';
        
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'Error inserting summary: %', SQLERRM;
        RAISE;
    END;
END;
$$;
