class BuyerNotFoundError(Exception):
    """Raised when a buyer is not found"""
    
    def __init__(self, buyer_id: int):
        self.buyer_id = buyer_id
        super().__init__(f"Buyer with id {buyer_id} not found")


class BuyerAlreadyExistsError(Exception):
    """Raised when a buyer already exists"""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Buyer with {field} '{value}' already exists")


class BuyerInvalidDataError(Exception):
    """Raised when buyer data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid buyer data: {message}")
