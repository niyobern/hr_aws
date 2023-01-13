from segno import helpers
qrcode = helpers.make_mecard(name='Shittu Olumide', email='me@example.com', phone='+123456789')
qrcode.designator
'3-L'
# Some params accept multiple values, like email, phone, url
qrcode = helpers.make_mecard(name='Shittu Olumide', 
                             email=('me@example.com', 'email@example.com'),
                             url=['http://www.example.com', 'https://example.come/~olu'])
qrcode.save('mycontact.png', scale=3)