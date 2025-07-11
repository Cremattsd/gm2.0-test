
import functools
import jwt
from flask import request, jsonify, current_app
from db import logger

def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing—don’t ghost me like an empty office space! 👻"}), 401

        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
            logger.info(f"Token validated for user {user_id}—they’re ready to roll in the CRE world! 🏢")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired—time to renew that lease! ⏰"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token—looks like a bad deal! 🚫"}), 401

        return f(user_id, *args, **kwargs)
    return decorated
