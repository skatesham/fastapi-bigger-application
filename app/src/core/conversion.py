"""
Generic conversion utilities for SQLAlchemy models to Pydantic schemas
Uses Pydantic's model_dump with exclude to eliminate manual converter layers
"""

from typing import List, Type, TypeVar, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T', bound=BaseModel)
M = TypeVar('M', bound=DeclarativeBase)


def convert_model_to_schema(
    db_model: M, 
    schema_class: Type[T], 
    field_mapping: Dict[str, str] | None = None,
    exclude_fields: List[str] | None = None,
    nested_objects: Dict[str, Type[BaseModel]] | None = None
) -> T:
    """
    Convert SQLAlchemy model to Pydantic schema using model_dump
    
    Args:
        db_model: SQLAlchemy model instance
        schema_class: Target Pydantic schema class
        field_mapping: Optional mapping of model field names to schema field names
        exclude_fields: Fields to exclude from the model dump
        nested_objects: Dict of nested object field names to their schema classes
    
    Returns:
        Pydantic schema instance
    """
    if db_model is None:
        return None
    
    # Get all model attributes from SQLAlchemy model
    model_data = {}
    
    # Get column names from SQLAlchemy model
    if hasattr(db_model, '__table__'):
        column_names = db_model.__table__.columns.keys()
    else:
        # Fallback: get all attributes that don't start with underscore
        column_names = [attr for attr in dir(db_model) if not attr.startswith('_')]
    
    # Handle field mapping and basic field extraction
    for field_name in column_names:
        # Skip private attributes and methods
        if field_name.startswith('_'):
            continue
            
        try:
            value = getattr(db_model, field_name)
        except (AttributeError, TypeError):
            continue
        
        # Skip callables (methods)
        if callable(value):
            continue
        
        # Apply field mapping if provided
        mapped_field_name = field_name
        if field_mapping and field_name in field_mapping:
            mapped_field_name = field_mapping[field_name]
        
        # Skip excluded fields
        if exclude_fields and mapped_field_name in exclude_fields:
            continue
            
        model_data[mapped_field_name] = value
    
    # Handle nested objects
    if nested_objects:
        for nested_field, nested_schema_class in nested_objects.items():
            # Get the prefix for nested fields (e.g., 'address_' for address fields)
            nested_data = {}
            nested_prefix = f"{nested_field}_"
            
            # Find all fields that belong to this nested object
            for field_name in column_names:
                if field_name.startswith(nested_prefix):
                    # Extract the nested field name (remove prefix)
                    nested_field_name = field_name[len(nested_prefix):]
                    try:
                        nested_data[nested_field_name] = getattr(db_model, field_name)
                    except (AttributeError, TypeError):
                        continue
            
            # Create nested schema instance
            if nested_data:
                model_data[nested_field] = nested_schema_class(**nested_data)
    
    # Create schema instance
    return schema_class(**model_data)


def convert_many_models_to_schemas(
    db_models: List[M], 
    schema_class: Type[T], 
    field_mapping: Dict[str, str] | None = None,
    exclude_fields: List[str] | None = None,
    nested_objects: Dict[str, Type[BaseModel]] | None = None
) -> List[T]:
    """
    Convert list of SQLAlchemy models to list of Pydantic schemas
    
    Args:
        db_models: List of SQLAlchemy model instances
        schema_class: Target Pydantic schema class
        field_mapping: Optional mapping of model field names to schema field names
        exclude_fields: Fields to exclude from the model dump
        nested_objects: Dict of nested object field names to their schema classes
    
    Returns:
        List of Pydantic schema instances
    """
    return [
        convert_model_to_schema(
            db_model, schema_class, field_mapping, exclude_fields, nested_objects
        )
        for db_model in db_models
    ]
