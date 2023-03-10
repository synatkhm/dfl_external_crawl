from fastapi_login import LoginManager
from src.utils.exception import NotAuthenticatedException

DB = {
    'users': {
    }
}
SECRET = "47C61A0FA8738BA77308A8A600F88E4B"
manager = LoginManager(SECRET, '/login', use_cookie=True, custom_exception=NotAuthenticatedException)

# user auth init
@manager.user_loader()
def load_user(user_id: str):
    user = DB['users'].get(user_id)
    return user   