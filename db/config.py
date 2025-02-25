import mysql.connector #type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")


def openConn():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DATABASE
    )
    cursor = connection.cursor()
    return connection, cursor

def closeConn(conn, cursor):
    cursor.close()
    conn.close()

def create_table():
    print("Creating or checking the 'leads' table...")
    connection, cursor = openConn()

    try:
        # Altera para o banco de dados 'employeespy'
        cursor.execute(f"USE {DATABASE}")

        # Defina a estrutura da tabela
       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            status_id VARCHAR(255),
            pipeline_id VARCHAR(255),
            price FLOAT,
            contact_id INT,          
            created_at TIMESTAMP
                       
        )
    """)
    
        connection.commit()

        print("Table 'leads' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)

def create_table_loss_reasons():
    print("Creating or checking the 'loss_reasons' table...")
    connection, cursor = openConn()

    try:
        # Altera para o banco de dados 'employeespy'
        cursor.execute(f"USE {DATABASE}")

        # Defina a estrutura da tabela
       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS loss_reasons (
            id INT,
            lead_id INT,
            loss_reason VARCHAR(255)    
        )
    """)
    
        connection.commit()

        print("Table 'leads' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)


def create_status_table():
    print("Creating or checking the 'status' table...")

    try:
        connection, cursor = openConn()
        # Altera para o banco de dados 'employeespy'
        cursor.execute(f"USE {DATABASE}")

        # Defina a estrutura da tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS statususes (
            id INTEGER,
            name VARCHAR(255),
            pipeline_id INTEGER
        )
    """)
    
        connection.commit()

        print("Table 'status' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)

def create_pipeline_table():
    print("Creating or checking the 'pipleine' table...")

    try:
        connection, cursor = openConn()
        # Altera para o banco de dados 'employeespy'
        cursor.execute(f"USE {DATABASE}")

        # Defina a estrutura da tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipelines (
            id INTEGER,
            name VARCHAR(255)
        )
    """)
    
        connection.commit()

        print("Table 'pipeline' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)

def create_contacts_table():
    print("Creating or checking the 'contacts' table...")

    try:
        connection, cursor = openConn()
        # Altera para o banco de dados 'employeespy'
        cursor.execute(f"USE {DATABASE}")

        # Defina a estrutura da tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            created_at VARCHAR(255),
            phone VARCHAR(255)
        )
    """)
    
        connection.commit()

        print("Table 'pipeline' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)

# Chama a função create_table quando este script é executado diretamente
if __name__ == "__main__":
    create_table()
    create_status_table()
    create_pipeline_table()
    create_contacts_table()
    create_table_loss_reasons()