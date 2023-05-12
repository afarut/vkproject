# Проект для стажировки VK

## Instalation
```bash
python -m venv env
pip install -r requirements.txt
```

## Rest Api
For example: http://localhost:8000

### Create User
Registration
```url
http://localhost:8000/createuser/
```

### Get JWT-Token
In my project i use jwt-tokens, so users must to get this token
```url
http://localhost:8000/api/token/
```

If you want to refresh, use it:
```url
http://localhost:8000/api/token/refresh/
```
**_NOTE:_** In every requests down the list you must to add the next header:
```url
Authorization: Bearer YOUR_TOKEN
```


### Get subscribers list
Getting list of people, which user rejected in last
```url
http://localhost:8000/subscribers/
```

### Get friends list
```url
http://localhost:8000/friends/
```

### Get all friend-requests
All friend-requests related with authorizan user
```url
http://localhost:8000/requests/
```

### Get relation info about people
```url
http://localhost:8000/user/pk/
```
Instead pk use integer value (user id). For example:
```url
http://localhost:8000/user/1/
```

### Delete from friends
```url
http://localhost:8000/user/delete/pk/
```
Instead pk use integer value (user id). For example:
```url
http://localhost:8000/user/delete/1/
```

### User send friend request
```url
http://localhost:8000/user/gofriend/pk/
```
Instead pk use integer value (user id). For example:
```url
http://localhost:8000/user/gofriend/1/
```
