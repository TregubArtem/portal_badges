# Portal Badges
Short project on Python. Main goal - is to send badges between participants in an automatic mode (after manual launch).

## How to use

### 1. Define "credentials.txt"
There should be 9 lines.
1. Method type
2. Path to corporate portal.
3. Part of endpoint that responsible for sending badges.
4. Part of endpoint that responsible for getting profile page.
5. Parameter key for sending id of profile.  
6. Parameter key for sending id of badge.  
7. Parameter key for sending welcome message.  
8. Parameter key for sending token of user.  
9. Parameter key for a cookie in headers.

### 2. Define "senders.txt"
There should be 3 lines per each sender. Also, no sense to define less than 2 senders.
Each line responsible for:
1. Profile id of sender.
2. Token used at badges endpoint.
3. Cookie value of sender's profile.

### 3. Launch main file
```
python3.8 main.py
```