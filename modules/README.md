All modules should must follow the below steps:

- Have their own folder
- Contain an "\__init\__" file
- Have two files - "module_bot.py" and "module_core.py"


#module_core.py

This file should have all the core logic for interacting with the endpoint. For example, the Facebook
module would have all the functions required to communicate with the
Messenger API.

This file should **NOT** contain any logic that involves decision logic
pertaining to user requests. That logic is place in module_bot.py


#module_bot.py

This file should contain the logic for handling users requests and
determining the responses. It is tightly coupled to the module_core.py
and makes extensive use of its functions.

This file should at least contain the following methods:

- ###```module_handle_user_request(request)```

This method would receive the incoming request from the service and
extract the user text. This text **MUST** be sent to Google for processing using
the following code:

```python
ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
if 'fulfillmentText' in ai_json_response:
    text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
    twitter_core.send_dm(sender_id, text_to_send)
```

In this method, the sender_id would be the identifier the particular service uses
to identify a user.

- ###```module_handle_df_request(request, session_id)```
This method should receive the response from the DialogFlow web service and handle it
accordingly. For this to work, the method must be registered in the
```dispatcher.py``` file 
