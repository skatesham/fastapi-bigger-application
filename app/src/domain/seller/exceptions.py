class SellerNotFoundError(Exception):
    """Raised when a seller is not found"""
    
    def __init__(self, seller_id: int):
        self.seller_id = seller_id
        super().__init__(f"Seller with id {seller_id} not found")


class SellerAlreadyExistsError(Exception):
    """Raised when a seller already exists"""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Seller with {field} '{value}' already exists")


class InvalidSellerError(Exception):
    """Raised when seller data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid seller data: {message}")
