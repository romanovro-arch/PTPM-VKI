def validate_password(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if ' ' in password:
        raise ValueError("Пароль не должен содержать пробелы")

    if len(password) > 20 or 8 > len(password):
        return False

    allowed_specials = set("!@#$%^&*")

    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_spec = any(char in allowed_specials for char in password)

    return has_upper and has_lower and has_digit and has_spec