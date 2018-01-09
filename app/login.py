from app import login_manager
from app.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)
