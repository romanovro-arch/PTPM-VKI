"""
Модуль собственного проекта из ЛР1 (согласно структуре README.md: src/my_project.py).
"""

from .auth_validator import mask_password, validate_registration

__all__ = ["mask_password", "validate_registration"]
