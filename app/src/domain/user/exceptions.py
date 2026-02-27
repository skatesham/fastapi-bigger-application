class UserNotFoundError(Exception):
    """Raised when a user is not found"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} not found")


class UserAlreadyExistsError(Exception):
    """Raised when a user already exists"""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"User with {field} '{value}' already exists")


class InvalidUserError(Exception):
    """Raised when user data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid user data: {message}")


class InactiveUserError(Exception):
    """Raised when trying to perform operation on inactive user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id {user_id} is inactive")


class ItemNotFoundError(Exception):
    """Raised when an item is not found"""
    
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item with id {item_id} not found")


class InvalidItemError(Exception):
    """Raised when item data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid item data: {message}")
