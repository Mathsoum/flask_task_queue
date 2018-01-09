class User:
    """
    Customer class for user management.
    Used with Flask-Login. See https://flask-login.readthedocs.io/en/latest/#your-user-class for basic
    documentation.
    """

    def __init__(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True
        self.id = u''

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        return None
