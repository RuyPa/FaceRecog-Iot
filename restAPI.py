from firebase.firebase import FirebaseApplication
app = FirebaseApplication('https://fir-fr.firebaseio.com/', authentication=None)
result = app.get('/users', None)

from firebase.firebase import FirebaseAuthentication
authentication = FirebaseAuthentication(
    secret='abcd1234',
    email='dobaduy.hungyen@gmail.com',
    extra={'id': 123}
)
app = FirebaseApplication('https://fir-fr.firebaseio.com/', authentication=authentication)
result = app.get('/users', None)
result
{'1': 'Minh', '2': 'Ha'}

result = app.get('/users', '1')
print(result)