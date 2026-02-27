from sqlalchemy.orm import Session

from . import exceptions, repository, schemas


class CarService:
    def __init__(self):
        self.car_repository = repository.car_repository

    def create_car(self, db: Session, car: schemas.CarCreate) -> schemas.Car:
        """Create a new car"""
        # Check if car with same name, year, and brand already exists
        existing_cars = self.car_repository.get_multi(db)
        for existing_car in existing_cars:
            if (existing_car.name == car.name and 
                existing_car.year == car.year and 
                existing_car.brand == car.brand):
                raise exceptions.CarAlreadyExistsError("name, year, brand", f"{car.name} {car.year} {car.brand}")
        
        # Create car
        db_car = self.car_repository.create(db, obj_in=car)
        return schemas.Car.from_model(db_car)

    def get_car(self, db: Session, car_id: int) -> schemas.Car:
        """Get car by ID"""
        db_car = self.car_repository.get_by_id(db, id=car_id)
        if db_car is None:
            raise exceptions.CarNotFoundError(car_id)
        
        return schemas.Car.from_model(db_car)

    def get_cars(self, db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Car]:
        """Get multiple cars with pagination"""
        db_cars = self.car_repository.get_multi(db, skip=skip, limit=limit)
        return schemas.Car.from_models(db_cars)

    def update_car(self, db: Session, car_id: int, car_update: schemas.CarUpdate) -> schemas.Car:
        """Update car"""
        db_car = self.car_repository.get_by_id(db, id=car_id)
        if db_car is None:
            raise exceptions.CarNotFoundError(car_id)
        
        # Check if update would create duplicate
        if any([car_update.name, car_update.year, car_update.brand]):
            update_data = car_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_car, field, value)
            
            # Check for duplicates after applying updates
            existing_cars = self.car_repository.get_multi(db)
            for existing_car in existing_cars:
                if (existing_car.id != car_id and
                    existing_car.name == db_car.name and 
                    existing_car.year == db_car.year and 
                    existing_car.brand == db_car.brand):
                    raise exceptions.CarAlreadyExistsError("name, year, brand", f"{db_car.name} {db_car.year} {db_car.brand}")
        
        # Update car
        updated_car = self.car_repository.update(db, db_obj=db_car, obj_in=car_update)
        return schemas.Car.from_model(updated_car)

    def delete_car(self, db: Session, car_id: int) -> bool:
        """Delete car"""
        try:
            self.car_repository.delete(db, id=car_id)
            return True
        except ValueError:
            raise exceptions.CarNotFoundError(car_id)

    def search_cars_by_brand(self, db: Session, brand: str) -> list[schemas.Car]:
        """Search cars by brand"""
        db_cars = self.car_repository.get_multi(db)
        filtered_cars = [car for car in db_cars if car.brand.lower() == brand.lower()]
        return schemas.Car.from_models(filtered_cars)


# Create singleton instance
car_service = CarService()
