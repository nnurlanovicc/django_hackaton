from django.core.mail import send_mail


def send_activation_code(email,activation_code):
    message = f'''
        добро пожаловать в memogram, вы успешно зарегались на нашем сайте. Для активации ващего аккаунта отпрвьте 
        нам этот код: {activation_code}
    '''
    send_mail('Активация аккаунта в Memogram',
        message,
        'memogram@gmail.com',
        [email]
    )