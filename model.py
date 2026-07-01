import os
import pymysql
from config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_db():
    """Create and return a TiDB/MySQL database connection."""
    if not Config.TIDB_HOST or not Config.TIDB_USER or not Config.TIDB_PASSWORD or not Config.TIDB_DB:
        raise RuntimeError(
            "TiDB configuration is required. Set TIDB_HOST, TIDB_USER, TIDB_PASSWORD, and TIDB_DB."
        )

    try:
        ca_path = Config.TIDB_SSL_CA

        if not ca_path:
            raise RuntimeError(
                "TiDB SSL CA path is required. Set TIDB_SSL_CA or TIDB_SSL_CA_B64 "
                "to a valid CA certificate for secure TiDB connections."
            )

        if not os.path.exists(ca_path):
            raise RuntimeError(
                f"TiDB SSL CA file not found: {ca_path}. Check TIDB_SSL_CA or "
                "TIDB_SSL_CA_B64 environment variable."
            )

        connect_kwargs = {
            'host': Config.TIDB_HOST,
            'port': Config.TIDB_PORT,
            'user': Config.TIDB_USER,
            'password': Config.TIDB_PASSWORD,
            'database': Config.TIDB_DB,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'ssl': {'ca': ca_path},
        }

        connection = pymysql.connect(**connect_kwargs)
        connection.__dict__['__db_backend'] = 'mysql'
        return connection
    except Exception as e:
        raise RuntimeError(f"Failed to connect to TiDB: {e}") from e


def init_db():
    """Initialize database tables and seed default portfolio data on TiDB."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    title VARCHAR(150),
                    bio TEXT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    location VARCHAR(100),
                    github VARCHAR(200),
                    linkedin VARCHAR(200),
                    instagram VARCHAR(200),
                    photo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            try:
                cur.execute("SHOW COLUMNS FROM profiles LIKE 'instagram'")
                if not cur.fetchone():
                    cur.execute("ALTER TABLE profiles ADD COLUMN instagram VARCHAR(200) AFTER linkedin")
            except Exception:
                pass

            cur.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50),
                    level INT DEFAULT 80,
                    icon VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company VARCHAR(150) NOT NULL,
                    position VARCHAR(150) NOT NULL,
                    start_date VARCHAR(20),
                    end_date VARCHAR(20),
                    is_current TINYINT(1) DEFAULT 0,
                    description TEXT,
                    logo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    tech_stack VARCHAR(300),
                    image_url VARCHAR(500),
                    demo_url VARCHAR(300),
                    repo_url VARCHAR(300),
                    is_featured TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    is_read TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            cur.execute("SELECT COUNT(*) as cnt FROM profiles")
            if cur.fetchone()['cnt'] == 0:
                cur.execute("""
                    INSERT INTO profiles (name, title, bio, email, phone, location, github, linkedin, photo_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    'Shafa Reyna Nugrahani',
                    'Mahasiswa S1 Sistem Informasi',
                    'Saya adalah pengembang web yang senang membuat portofolio dan aplikasi yang nyaman digunakan.',
                    'shafareynana@gmail.com',
                    '+62 812-3456-7890',
                    'Salatiga, Indonesia',
                    'https://github.com',
                    'https://linkedin.com',
                    'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=800&q=80'
                ))

            conn.commit()
    finally:
        conn.close()


def get_profiles():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM profiles")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting profiles: {e}")
        return []


def get_skills():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM skills")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting skills: {e}")
        return []


def get_projects():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM projects")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        return []


def get_experience():
    try:
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM experiences")
                result = cur.fetchall()
            return result if result else []
        finally:
            conn.close()
    except Exception as e:
        print(f"❌ Error getting experiences: {e}")
        return []
