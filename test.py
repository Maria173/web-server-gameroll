from requests import get, post, delete

cookies = dict(session='Session cookies here')
print(post('http://localhost:8000/api/v1/characters',
           json={'title': 'Туг', 'name': 'Gendalf', 'city': 'Георам',
                 'age': 59, 'info': '', 'ispublic': True, 'user_id': 1}, cookies=cookies).json())
print(get('http://localhost:8000/api/v1/characters').json())
print(delete('http://localhost:8000/api/v1/characters/1', cookies=cookies).json())
print(get('http://localhost:8000/api/v1/characters').json())
