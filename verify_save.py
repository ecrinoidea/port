from app import app

client = app.test_client()
client.session_transaction().update({'admin_logged_in': True})
resp = client.post('/api/admin/profiles', json={
    'name': 'Flow Test Profile',
    'title': 'Developer',
    'bio': 'Inserted from verification',
    'email': 'flow@example.com',
    'phone': '08123456789',
    'location': 'Jakarta',
    'github': 'https://github.com/example',
    'linkedin': 'https://linkedin.com/in/example',
    'photo_url': 'https://example.com/profile.jpg'
})
print('POST_STATUS', resp.status_code)
print('POST_JSON', resp.get_json())
pub = client.get('/api/profile')
print('PUBLIC_STATUS', pub.status_code)
print('PUBLIC_JSON', pub.get_json())
