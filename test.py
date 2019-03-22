from requests import get, post, delete

cookies = dict(session='Session cookies here')
print(post('http://localhost:8000/api/v1/characters',
           json={'title': 'Заголовок', 'name': 'Текст новости', 'city': 'aaaa',
                 'age': 25, 'info': 'nit', 'ispublic': True, 'user_id': 1}, cookies=cookies).json())
print(get('http://localhost:8000/api/v1/characters').json())
print(delete('http://localhost:8000/api/v1/characters/2', cookies=cookies).json())
print(get('http://localhost:8000/api/v1/characters').json())
