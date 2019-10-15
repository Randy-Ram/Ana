#Ana
Ana is a bot-platform that integrates various messaging platforms into one 
cohesive interface. It uses Dialogflow for NLP processing.

#Platforms Supported
* Facebook
* Twitter
* Slack
* Whatsapp (in beta via Twilio)
* Kommunicate


#Architecture

![Ana Architecture](https://i.imgur.com/hodztrI.png)


## Chat Flow
1. User initiates requests from a particular platform to a particular endpoint
on a web server.
2. The request is handled by the platform's 'bot' module and the request is forwarded
to Dialogflow
3. Dialogflow then responds to the web server and the Dispatcher module will parse
the response and send to the appropriate platform 'bot' module.
4. The 'bot' module either calls external API's if it needs to, or calls the 
'core' module logic to communicate to the user.

