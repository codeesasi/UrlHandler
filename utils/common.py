from datetime import datetime, UTC
import psycopg2

def get_current_utc_datetime() -> datetime:
    """
    Returns the current time in UTC.
    
    :return: Current time in UTC.
    """
    return datetime.now(UTC).isoformat()

def connect_pgdb():
    """
    Placeholder function for database connection.
    Replace with actual database connection logic.
    
    :return: Database connection object.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="sasi1234",
            host="localhost",
            port="5432"
        )
        return conn.cursor()
    
    except ImportError:
        raise ImportError("psycopg2 is not installed. Please install it using 'pip install psycopg2-binary'.")
    
    except Exception as e:
        raise Exception(f"Failed to connect to the database: {str(e)}")
    
def clipboard_safe_insert(url: str,title: str,thumbnail: str) -> bool:
    """
    Safely inserts clipboard data into the database.
    
    :param clipboard_data: Data to be inserted.
    :return: True if insertion is successful, False otherwise.
    """
    try:
        cursor = connect_pgdb()
        cursor.execute("SELECT fn_insert_url(%s, %s, %s);", (url, title, thumbnail))
        cursor.connection.commit()  # Commit the transaction
        result = cursor.fetchone()[0]
        return result
    except Exception as e:
        print(f"Error inserting clipboard data: {e}")
        return 'Error inserting data'
    
    finally:
        if cursor:
            cursor.close()