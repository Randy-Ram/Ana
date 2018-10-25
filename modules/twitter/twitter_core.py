import base64
import hashlib
import hmac
import json
from config import twitter_consumer_secret


def webhook_challenge(request):
    # creates HMAC SHA-256 hash from incoming token and your consumer secret
    # encoded_secret = twitter_consumer_secret.encode("utf-8")
    sha256_hash_digest = hmac.new(twitter_consumer_secret.encode("utf-8"), msg=request.args.get('crc_token').encode('utf-8'),
                                  digestmod=hashlib.sha256).digest()
    # construct response data with base64 encoded hash
    response = {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('ascii')
    }

    # returns properly formatted json response
    print(response)
    return json.dumps(response)