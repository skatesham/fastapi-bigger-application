from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import exceptions, repository, schemas


class StockService:
    def __init__(self):
        self.stock_repository = repository.stock_repository

    def create_stock(self, db: Session, stock: schemas.StockCreate) -> schemas.Stock:
        """Create a new stock"""
        # Check if car exists
        from app.src.domain.car.repository import car_repository
        from app.src.domain.car.exceptions import CarNotFoundError
        car = car_repository.get_by_id(db, id=stock.car_id)
        if not car:
            raise CarNotFoundError(stock.car_id)
        
        # Check if stock already exists for this car
        existing_stock = self.stock_repository.get_by_car_id(db, car_id=stock.car_id)
        if existing_stock:
            raise exceptions.StockAlreadyExistsError(stock.car_id)
        
        # Create stock
        db_stock = self.stock_repository.create(db, obj_in=stock)
        # Refresh to load relationships
        db.refresh(db_stock)
        return db_stock

    def get_stock(self, db: Session, stock_id: int) -> schemas.Stock:
        """Get stock by ID"""
        db_stock = self.stock_repository.get_by_id(db, id=stock_id)
        if db_stock is None:
            raise exceptions.StockNotFoundError(stock_id)
        
        return db_stock

    def get_stock_by_car(self, db: Session, car_id: int) -> schemas.Stock:
        """Get stock by car ID"""
        db_stock = self.stock_repository.get_by_car_id(db, car_id=car_id)
        if db_stock is None:
            raise exceptions.StockNotFoundError(0)  # Car lookup, no stock ID
        
        return db_stock

    def buy_car_from_stock(self, db: Session, car_id: int, quantity: int) -> schemas.Stock:
        """Buy car from stock (reduce quantity)"""
        db_stock = self.stock_repository.get_by_car_id(db, car_id=car_id)
        if db_stock is None:
            raise exceptions.StockNotFoundError(0)
        
        if not db_stock.hasStock(quantity):
            raise exceptions.InsufficientStockError(car_id, quantity, db_stock.quantity)
        
        # Reduce quantity
        db_stock.reduce_quantity(quantity)
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock

    def get_stocks(self, db: Session) -> Page[schemas.Stock]:
        """Get all stocks with pagination"""
        from .models import Stock
        return paginate(db, select(Stock).order_by(Stock.id))

    def update_stock(self, db: Session, stock_id: int, stock_update: schemas.StockUpdate) -> schemas.Stock:
        """Update stock"""
        db_stock = self.stock_repository.get_by_id(db, id=stock_id)
        if db_stock is None:
            raise exceptions.StockNotFoundError(stock_id)
        
        # Check if car_id is being updated and already exists
        if stock_update.car_id and stock_update.car_id != db_stock.car_id:
            existing_stock = self.stock_repository.get_by_car_id(db, car_id=stock_update.car_id)
            if existing_stock:
                raise exceptions.StockAlreadyExistsError(stock_update.car_id)
        
        # Update stock
        updated_stock = self.stock_repository.update(db, db_obj=db_stock, obj_in=stock_update)
        return schemas.Stock.from_model(updated_stock)

    def delete_stock(self, db: Session, stock_id: int) -> bool:
        """Delete stock"""
        try:
            self.stock_repository.delete(db, id=stock_id)
            return True
        except ValueError:
            raise exceptions.StockNotFoundError(stock_id)

    def get_low_stock_items(self, db: Session, threshold: int = 5) -> list[schemas.Stock]:
        """Get stocks with quantity below threshold"""
        db_stocks = self.stock_repository.get_low_stock(db, threshold=threshold)
        return db_stocks

    def get_available_stocks(self, db: Session) -> list[schemas.Stock]:
        """Get all stocks with quantity > 0"""
        db_stocks = self.stock_repository.get_available_stock(db)
        return db_stocks


# Create singleton instance
stock_service = StockService()
