class SaleNotFoundError(Exception):
    """Raised when a sale is not found"""
    
    def __init__(self, sale_id: int):
        self.sale_id = sale_id
        super().__init__(f"Sale with id {sale_id} not found")


class InvalidSaleError(Exception):
    """Raised when sale data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid sale: {message}")


class CarNotAvailableError(Exception):
    """Raised when car is not available for sale"""
    
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car with id {car_id} is not available for sale")
