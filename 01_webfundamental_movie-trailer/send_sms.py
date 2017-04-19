from twilio.rest import TwilioRestClient

account_sid = "AC270d45b03bdee67fefe236ce9ad17347" # Your Account SID from www.twilio.com/console
auth_token  = "a68428b261717b3e73aacc0df9b68e5e"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="Hello from Erik, ngoau!",
    to="+6585123464",    # Replace with your phone number
    from_="+19494852513") # Replace with your Twilio number

print(message.sid)