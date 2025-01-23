import requests
import os

# API server address and port
api_address = 'start_api_container'#'api'#'localhost'
api_port = 8000
api_url = os.environ.get('API_URL')

# User credentials and expected outcomes
users = [
    {"username": "alice", "password": "wonderland", "expected_status": 200},
    {"username": "bob", "password": "builder", "expected_status": 200},
    {"username": "clementine", "password": "mandarine", "expected_status": 403}
]

output = '''
============================
    Authentication Test
============================
request done at "/permissions"
| username="{username}"
| password="{password}"
expected result = {expected_status}
actual result = {status_code}
==>  {test_status}
'''

# Loop through the users and test authentication
for user in users:
    r = requests.get(
        url=f'{api_url}/permissions',
        params={
            'username': user["username"],
            'password': user["password"]
        }
    )
    
    status_code = r.status_code
    test_status = 'SUCCESS' if status_code == user["expected_status"] else 'FAILURE'
    
    # Print result
    print(output.format(
        username=user["username"],
        password=user["password"],
        expected_status=user["expected_status"],
        status_code=status_code,
        test_status=test_status
    ))

    # Save to log if LOG environment variable is set
    if os.environ.get('LOG') == '1':
        with open('/app/logs/authentication_test.log', 'a') as file:
            file.write(output.format(
                username=user["username"],
                password=user["password"],
                expected_status=user["expected_status"],
                status_code=status_code,
                test_status=test_status
            ))
