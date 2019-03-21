from requests import get, post, delete

cookies = dict(session='eyJjc3JmX3Rva2VuIjoiY2U1NzhjMTY0Mzk4MDQ2NDQxMzNlNGUxOWY3ZTVlMzEzNTEyMTRhZiIsInVzZXJfaWQiOjN9.XJPWOQ.bwG1s40ftRXM1oozRXDiVoWYfnQ')
print(post('http://localhost:8000/api/v1/news',
           json={'title': 'Заголовок', 'name': 'Текст новости', 'city': 'aaaa',
                 'age': 25, 'info': 'nit', 'ispublic': True, 'user_id': 1}, cookies=cookies).json())
print(get('http://localhost:8000/api/v1/news').json())
print(delete('http://localhost:8000/api/v1/news/2', cookies=cookies).json())
print(get('http://localhost:8000/api/v1/news').json())
