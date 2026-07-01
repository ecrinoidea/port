"""
Script untuk memperbaiki struktur database
Ini akan drop tabel lama dan recreate dengan struktur yang benar
"""

from model import get_db

def fix_database():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            # Drop tabel lama jika ada
            print("Dropping old tables...")
            cur.execute("DROP TABLE IF EXISTS contacts")
            cur.execute("DROP TABLE IF EXISTS projects")
            cur.execute("DROP TABLE IF EXISTS experiences")
            cur.execute("DROP TABLE IF EXISTS skills")
            cur.execute("DROP TABLE IF EXISTS profiles")
            print("✓ Old tables dropped")
            
            # Create profiles table dengan struktur yang benar
            print("\nCreating profiles table...")
            cur.execute("""
                CREATE TABLE profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    title VARCHAR(150),
                    bio TEXT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    location VARCHAR(100),
                    github VARCHAR(200),
                    linkedin VARCHAR(200),
                    photo_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ Profiles table created")
            
            # Create skills table
            print("Creating skills table...")
            cur.execute("""
                CREATE TABLE skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(50),
                    level INT DEFAULT 80,
                    icon VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ Skills table created")
            
            # Create experiences table
            print("Creating experiences table...")
            cur.execute("""
                CREATE TABLE experiences (
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
            print("✓ Experiences table created")
            
            # Create projects table
            print("Creating projects table...")
            cur.execute("""
                CREATE TABLE projects (
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
            print("✓ Projects table created")
            
            # Create contacts table
            print("Creating contacts table...")
            cur.execute("""
                CREATE TABLE contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    is_read TINYINT(1) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✓ Contacts table created")
            
            # Insert default data
            print("\nInserting default data...")
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
            print("✓ Default profile inserted")
            
            # Insert default skills
            cur.execute("""
                INSERT INTO skills (name, category, level, icon) VALUES
                (%s, %s, %s, %s),
                (%s, %s, %s, %s),
                (%s, %s, %s, %s),
                (%s, %s, %s, %s),
                (%s, %s, %s, %s)
            """, (
                'Python', 'Backend', 90, 'python',
                'Flask', 'Backend', 85, 'flask',
                'JavaScript', 'Frontend', 88, 'javascript',
                'MySQL', 'Database', 80, 'mysql',
                'Git', 'Tools', 82, 'git'
            ))
            print("✓ Default skills inserted")
            
            conn.commit()
            print("\n✓ Database fixed successfully!")
            return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("="*50)
    print("DATABASE FIX SCRIPT")
    print("="*50)
    fix_database()
