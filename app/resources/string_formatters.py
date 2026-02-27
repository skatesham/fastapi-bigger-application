"""
String formatting utilities for dynamic exception messages
"""

from app.resources.strings import (
    # Not Found Templates
    CAR_NOT_FOUND_TEMPLATE,
    BUYER_NOT_FOUND_TEMPLATE,
    SELLER_NOT_FOUND_TEMPLATE,
    STOCK_NOT_FOUND_TEMPLATE,
    USER_NOT_FOUND_TEMPLATE,
    SALE_NOT_FOUND_TEMPLATE,
    ITEM_NOT_FOUND_TEMPLATE,
    
    # Already Exists Templates
    CAR_ALREADY_EXISTS_TEMPLATE,
    BUYER_ALREADY_EXISTS_TEMPLATE,
    SELLER_ALREADY_EXISTS_TEMPLATE,
    USER_ALREADY_EXISTS_TEMPLATE,
    STOCK_ALREADY_EXISTS_TEMPLATE,
    
    # Invalid Data Templates
    INVALID_BUYER_DATA_TEMPLATE,
    INVALID_SELLER_DATA_TEMPLATE,
    INVALID_STOCK_DATA_TEMPLATE,
    INVALID_USER_DATA_TEMPLATE,
    INVALID_SALE_DATA_TEMPLATE,
    INVALID_ITEM_DATA_TEMPLATE,
    
    # Business Logic Templates
    CAR_NOT_AVAILABLE_TEMPLATE,
    INSUFFICIENT_STOCK_TEMPLATE,
    INACTIVE_USER_TEMPLATE,
)


def format_car_not_found(car_id: int) -> str:
    """Format car not found message"""
    return CAR_NOT_FOUND_TEMPLATE.format(id=car_id)


def format_buyer_not_found(buyer_id: int) -> str:
    """Format buyer not found message"""
    return BUYER_NOT_FOUND_TEMPLATE.format(id=buyer_id)


def format_seller_not_found(seller_id: int) -> str:
    """Format seller not found message"""
    return SELLER_NOT_FOUND_TEMPLATE.format(id=seller_id)


def format_stock_not_found(stock_id: int) -> str:
    """Format stock not found message"""
    return STOCK_NOT_FOUND_TEMPLATE.format(id=stock_id)


def format_user_not_found(user_id: int) -> str:
    """Format user not found message"""
    return USER_NOT_FOUND_TEMPLATE.format(id=user_id)


def format_sale_not_found(sale_id: int) -> str:
    """Format sale not found message"""
    return SALE_NOT_FOUND_TEMPLATE.format(id=sale_id)


def format_item_not_found(item_id: int) -> str:
    """Format item not found message"""
    return ITEM_NOT_FOUND_TEMPLATE.format(id=item_id)


def format_car_already_exists(field: str, value: str) -> str:
    """Format car already exists message"""
    return CAR_ALREADY_EXISTS_TEMPLATE.format(field=field, value=value)


def format_buyer_already_exists(field: str, value: str) -> str:
    """Format buyer already exists message"""
    return BUYER_ALREADY_EXISTS_TEMPLATE.format(field=field, value=value)


def format_seller_already_exists(field: str, value: str) -> str:
    """Format seller already exists message"""
    return SELLER_ALREADY_EXISTS_TEMPLATE.format(field=field, value=value)


def format_user_already_exists(field: str, value: str) -> str:
    """Format user already exists message"""
    return USER_ALREADY_EXISTS_TEMPLATE.format(field=field, value=value)


def format_stock_already_exists(car_id: int) -> str:
    """Format stock already exists message"""
    return STOCK_ALREADY_EXISTS_TEMPLATE.format(car_id=car_id)


def format_invalid_buyer_data(message: str) -> str:
    """Format invalid buyer data message"""
    return INVALID_BUYER_DATA_TEMPLATE.format(message=message)


def format_invalid_seller_data(message: str) -> str:
    """Format invalid seller data message"""
    return INVALID_SELLER_DATA_TEMPLATE.format(message=message)


def format_invalid_stock_data(message: str) -> str:
    """Format invalid stock data message"""
    return INVALID_STOCK_DATA_TEMPLATE.format(message=message)


def format_invalid_user_data(message: str) -> str:
    """Format invalid user data message"""
    return INVALID_USER_DATA_TEMPLATE.format(message=message)


def format_invalid_sale_data(message: str) -> str:
    """Format invalid sale data message"""
    return INVALID_SALE_DATA_TEMPLATE.format(message=message)


def format_invalid_item_data(message: str) -> str:
    """Format invalid item data message"""
    return INVALID_ITEM_DATA_TEMPLATE.format(message=message)


def format_car_not_available(car_id: int) -> str:
    """Format car not available message"""
    return CAR_NOT_AVAILABLE_TEMPLATE.format(car_id=car_id)


def format_insufficient_stock(car_id: int, requested: int, available: int) -> str:
    """Format insufficient stock message"""
    return INSUFFICIENT_STOCK_TEMPLATE.format(
        car_id=car_id, 
        requested=requested, 
        available=available
    )


def format_inactive_user(user_id: int) -> str:
    """Format inactive user message"""
    return INACTIVE_USER_TEMPLATE.format(user_id=user_id)
