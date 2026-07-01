import os
import json

# Set test environment variables early so Config reads them during import
# Use a harmless localhost value so imports won't raise when DB isn't available.
os.environ.setdefault('TIDB_HOST', '127.0.0.1')
os.environ.setdefault('TIDB_USER', 'root')
os.environ.setdefault('TIDB_PASSWORD', '')
os.environ.setdefault('TIDB_DB', 'db_porto')

from app import app
from model import get_db

# Test login
print("=== TESTING LOGIN ===")
client = app.test_client()
login_res = client.post('/admin/login', json={'username': 'admin', 'password': 'admin123'})
print(f"Login status: {login_res.status_code}")
print(f"Login response: {login_res.get_json()}")

# Test profile save
print("\n=== TESTING PROFILE SAVE ===")
save_payload = {
    'name': 'Shafa Reyna Nugrahani',
    'title': 'Mahasiswa S1 Sistem Informasi',
    'bio': 'Saya adalah pengembang web yang senang membuat portofolio.',
    'email': 'shafareynana@gmail.com',
    'phone': '08123456789',
    'location': 'Salatiga, Indonesia',
    'github': 'https://github.com/shafareyna',
    'linkedin': 'https://linkedin.com/in/shafareyna',
    'photo_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=800&q=80'
}

# Make authenticated request
with client:
    # First login in the same session
    client.post('/admin/login', json={'username': 'admin', 'password': 'admin123'})
    
    # Then save profile
    save_res = client.post('/api/admin/profiles', json=save_payload)
    print(f"Save status: {save_res.status_code}")
    print(f"Save response: {save_res.get_json()}")
    
    # Verify profile exists
    get_res = client.get('/api/admin/profiles')
    print(f"\nGet all profiles status: {get_res.status_code}")
    profiles = get_res.get_json()
    print(f"Profiles count: {len(profiles.get('data', []))}")
    print(f"First profile: {profiles['data'][0] if profiles.get('data') else 'None'}")
    
    # Test public endpoint
    print("\n=== TESTING PUBLIC ENDPOINT ===")
    pub_res = client.get('/api/profile')
    print(f"Public profile status: {pub_res.status_code}")
    print(f"Public profile data: {pub_res.get_json()}")

# Clean up
print("\n=== CLEANUP ===")
conn = get_db()
try:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM profiles WHERE name=%s", ('Shafa Reyna Nugrahani',))
    conn.commit()
    print("Test data cleaned up")
finally:
    conn.close()
