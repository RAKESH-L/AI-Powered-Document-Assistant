import mysql.connector
from mysql.connector import Error
from config import Config

def create_connection():
    """Create a database connection to a MySQL database"""
    try:
        connection = mysql.connector.connect(
            # host='your_host',
            # user='your_username',
            # password='your_password'
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USERNAME,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE_NAME,
            port=Config.MYSQL_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_database():
    """Create the database if it doesn't exist"""
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS documentassistent")
        cursor.execute("USE documentassistent")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        print(f"Error while creating database or table: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_connection_to_db():
    """Create a connection to the specific database"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USERNAME,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE_NAME,
            port=Config.MYSQL_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def store_embedding(text, embedding):
    """Store embedding in the database"""
    if not is_valid_embedding(embedding):
        print("Invalid embedding data. Skipping storage.")
        return
    
    connection = create_connection_to_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        # Convert embedding list to a string format
        embedding_str = ','.join(map(str, embedding))
        query = "INSERT INTO embeddings (text, embedding) VALUES (%s, %s)"
        cursor.execute(query, (text, embedding_str))
        connection.commit()
    except Error as e:
        print(f"Error while storing embedding: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def is_valid_embedding(embedding):
    """Validate the embedding to ensure it is complete and correct"""
    if not isinstance(embedding, list):
        return False
    if not all(isinstance(x, (float, int)) for x in embedding):
        return False
    return True

def get_embedding(text):
    """Retrieve embedding from the database"""
    
    connection = create_connection_to_db()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        query = "SELECT embedding FROM embeddings WHERE text = %s"
        cursor.execute(query, (text,))
        result = cursor.fetchone()
        cursor.fetchall()  # Fetch all remaining rows to clear the result set
        if result:
            # Convert string format back to list of floats
            embedding_str = result[0]
            embedding = list(map(float, embedding_str.split(',')))
            return embedding
        else:
            return None
    except Error as e:
        print(f"Error while retrieving embedding: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()