from django.apps import AppConfig

# ApppConfig occurs when we start the server
# it tells the server how the app is to be configured. 
# such as name, what is the deafult field value etc. 
class UserLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_login'
    verbose_name = "sid login"
