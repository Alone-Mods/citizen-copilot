from .health import health_bp
from .auth import auth_bp
from .profile import profile_bp
from .schemes import schemes_bp
from .documents import documents_bp
from .notifications import notifications_bp
from .ai import ai_bp

__all__ = [
    "health_bp",
    "auth_bp",
    "profile_bp",
    "schemes_bp",
    "documents_bp",
    "notifications_bp",
    "ai_bp"
]
