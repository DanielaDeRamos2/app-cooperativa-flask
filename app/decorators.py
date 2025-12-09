from functools import wraps
from flask import abort
from flask_login import current_user

def require_role(*roles):
    """Decorator para verificar se o usuário tem o tipo correto"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            user_type = current_user.tipo_usuario.value
            if user_type not in roles:
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
