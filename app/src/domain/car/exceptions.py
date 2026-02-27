class CarNotFoundError(Exception):
    """Raised when a car is not found"""
    
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car with id {car_id} not found")


class CarAlreadyExistsError(Exception):
    """Raised when a car already exists"""
    
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Car with {field} '{value}' already exists")
