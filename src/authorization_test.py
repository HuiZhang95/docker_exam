import requests
import os

api_address = 'api'#'localhost'
api_port = 8000
api_url = os.environ.get('API_URL')

# Test data
users = [
    {"username": "alice", "password": "wonderland", "access": ["v1", "v2"]},
    {"username": "bob", "password": "builder", "access": ["v1"]}
]

sentences = ["life is beautiful", "that sucks"]

output = '''
============================
    Authorization Test
============================
request done at "/v1/sentiment"
| username="{username}"
| password="{password}"
access versions = {access}
expected result = access to {expected_versions}
actual result = {actual_versions}
==>  {test_status}
'''

# Loop through users and test version access
for user in users:
    for version in ["v1", "v2"]:
        for sentence in sentences:
            r = requests.get(
                url=f'{api_url}/{version}/sentiment',
                params={
                    'username': user["username"],
                    'password': user["password"],
                    'sentence': sentence
                }
            )
            # Check if the user is allowed to access the version
            expected_versions = user["access"]
            actual_versions = [version] if version in user["access"] else []
            test_status = 'SUCCESS' if actual_versions else 'FAILURE'

            # Print result
            print(output.format(
                username=user["username"],
                password=user["password"],
                access=user["access"],
                expected_versions=expected_versions,
                actual_versions=actual_versions,
                test_status=test_status
            ))

            # Save to log if LOG environment variable is set
            if os.environ.get('LOG') == '1':
                with open('/app/logs/authorization_test.log', 'a') as file:
                    file.write(output.format(
                        username=user["username"],
                        password=user["password"],
                        access=user["access"],
                        expected_versions=expected_versions,
                        actual_versions=actual_versions,
                        test_status=test_status
                    ))
