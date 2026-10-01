# import bcrypt
# a='password'
# encoded=a.encode('utf-8')
# salt=bcrypt.gensalt(rounds=12)
# hashed=bcrypt.hashpw(encoded,salt)
# b='password'
# encoded1=b.encode('utf-8')
# if bcrypt.checkpw(encoded1,hashed):
#     print('success')
# else:
#     print('fail')


import jwt
import datetime

secret_key="hey there how are you"

payload = {
    "user_id":1,
    "username": 'ajay',
    "role": 'HR',
    "exp": datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(hours=1)
}

token=jwt.encode(payload,secret_key,algorithm='HS256')
print(token)

payload=jwt.decode(token,secret_key,algorithms='HS256')
print(payload)






