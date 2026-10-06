from flask_login import LoginManager , UserMixin

login_manager = LoginManager()

class User(UserMixin):

    def __init__(self , username):
        self.id = username



@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

