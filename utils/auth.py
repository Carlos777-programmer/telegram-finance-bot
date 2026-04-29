from config.settings import USER_ID

def autorizado(user_id: int) -> bool:
    return user_id == USER_ID