import requests
import os

api_address = 'api'#'localhost'
api_port = 8000
api_url = os.environ.get('API_URL')

# Sentences for testing
sentences = ["life is beautiful", "that sucks"]

output = '''
============================
    Content Test
============================
request done at "/v1/sentiment" and "/v2/sentiment"
| sentence = "{sentence}"
expected result = positive for "life is beautiful", negative for "that sucks"
actual result = v1: {v1_score}, v2: {v2_score}
==>  {test_status}
'''

# Test for each sentence and both versions
for sentence in sentences:
    for version in ["v1", "v2"]:
        r = requests.get(
            url=f'{api_url}/{version}/sentiment',
            params={
                'username': 'alice',
                'password': 'wonderland',
                'sentence': sentence
            }
        )
        
        # Check sentiment score: positive if score > 0, negative if score < 0
        sentiment_score = r.json().get('score', 0)
        score_status = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"

        # Print result
        print(output.format(
            sentence=sentence,
            v1_score=sentiment_score if version == "v1" else "N/A",
            v2_score=sentiment_score if version == "v2" else "N/A",
            test_status="SUCCESS" if score_status != "neutral" else "FAILURE"
        ))

        # Save to log if LOG environment variable is set
        if os.environ.get('LOG') == '1':
            with open('/app/logs/content_test.log', 'a') as file:
                file.write(output.format(
                    sentence=sentence,
                    v1_score=sentiment_score if version == "v1" else "N/A",
                    v2_score=sentiment_score if version == "v2" else "N/A",
                    test_status="SUCCESS" if score_status != "neutral" else "FAILURE"
                ))
