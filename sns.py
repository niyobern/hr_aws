import boto3
from random import random
import math

list = []
for i in range(6):
    x = 10 * random()
    y = math.floor(x)
    list.append(str(y))
otp = ''.join(list)
print(otp)

client = boto3.client(
    "sns",
    aws_access_key_id="AKIAWCJGOJN2DIEYFHFM",
    aws_secret_access_key="aHXeZutSw6I6O/Luv5UFfj0ehegiU/VTOkkKi+85",
    region_name="us-east-1"
)

# Send your sms message.
a = client.publish(
    PhoneNumber="+250786082841",
    Message= f"Your CUR Verification code is {otp} ",
    MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String',
                                                'StringValue': 'CUR' }}
)

print(a)