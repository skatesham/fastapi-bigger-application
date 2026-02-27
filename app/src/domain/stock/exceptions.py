class StockNotFoundError(Exception):
    """Raised when stock is not found"""
    
    def __init__(self, stock_id: int):
        self.stock_id = stock_id
        super().__init__(f"Stock with id {stock_id} not found")


class InsufficientStockError(Exception):
    """Raised when there's not enough stock"""
    
    def __init__(self, car_id: int, requested: int, available: int):
        self.car_id = car_id
        self.requested = requested
        self.available = available
        super().__init__(f"Insufficient stock for car {car_id}: requested {requested}, available {available}")


class StockAlreadyExistsError(Exception):
    """Raised when stock already exists for a car"""
    
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Stock already exists for car with id {car_id}")


class InvalidStockError(Exception):
    """Raised when stock data is invalid"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Invalid stock data: {message}")
