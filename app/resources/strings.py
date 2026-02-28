###
# Centralize response messages
###

# Errors - Resource Not Found (404)
CAR_DOES_NOT_EXIST_ERROR = "car does not exist"
STOCK_DOES_NOT_EXIST_ERROR = "stock does not exist"
BUYER_DOES_NOT_EXIST_ERROR = "buyer does not exist"
SELLER_DOES_NOT_EXIST_ERROR = "seller does not exist"
SALES_DOES_NOT_EXIST_ERROR = "sale does not exist"
USER_DOES_NOT_EXIST_ERROR = "user does not exist"
ITEM_DOES_NOT_EXIST_ERROR = "item does not exist"

# Errors - Resource Already Exists (409)
CAR_ALREADY_EXISTS_ERROR = "car already exists"
BUYER_ALREADY_EXISTS_ERROR = "buyer already exists"
SELLER_ALREADY_EXISTS_ERROR = "seller already exists"
STOCK_ALREADY_EXISTS_ERROR = "stock already exists"
USER_ALREADY_EXISTS_ERROR = "user already exists"
EMAIL_ALREADY_REGISTERED_ERROR = "Email already registered"

# Errors - Invalid Data (400)
INVALID_USER_ERROR = "Invalid user data"
INVALID_BUYER_ERROR = "Invalid buyer data"
INVALID_SELLER_ERROR = "Invalid seller data"
INVALID_STOCK_ERROR = "Invalid stock data"
INVALID_SALE_ERROR = "Invalid sale data"
INVALID_ITEM_ERROR = "Invalid item data"

# Errors - Business Logic (422)
CAR_NOT_AVAILABLE_ERROR = "Car not available"
STOCK_OUT_OF_STOCK_ERROR = "out of stock"
INSUFFICIENT_STOCK_ERROR = "Insufficient stock"
INACTIVE_USER_ERROR = "User is inactive"

# Authentication & Authorization Errors
UNAUTHORIZED_ERROR = "Unauthorized"

# Success Messages
ADMIN_SUCCESS_MESSAGE = "Admin getting schwifty"
CAR_CREATED_SUCCESS = "Car created successfully"
BUYER_CREATED_SUCCESS = "Buyer created successfully"
SELLER_CREATED_SUCCESS = "Seller created successfully"
STOCK_CREATED_SUCCESS = "Stock created successfully"
USER_CREATED_SUCCESS = "User created successfully"
SALE_CREATED_SUCCESS = "Sale created successfully"

# Generic Messages
RESOURCE_CREATED = "Resource created successfully"
RESOURCE_UPDATED = "Resource updated successfully"
RESOURCE_DELETED = "Resource deleted successfully"
RESOURCE_FOUND = "Resource found successfully"
RESOURCES_FOUND = "Resources found successfully"

# Validation Messages
VALIDATION_ERROR = "Validation failed"
MISSING_REQUIRED_FIELD = "Missing required field"
INVALID_FIELD_FORMAT = "Invalid field format"
FIELD_TOO_LONG = "Field exceeds maximum length"
FIELD_TOO_SHORT = "Field below minimum length"

# Database Messages
DATABASE_CONNECTION_ERROR = "Database connection failed"
DATABASE_ERROR = "Database operation failed"
MIGRATION_ERROR = "Database migration failed"

# Service Messages
SERVICE_UNAVAILABLE = "Service temporarily unavailable"
INTERNAL_SERVER_ERROR = "Internal server error"
REQUEST_TIMEOUT = "Request timeout"
RATE_LIMIT_EXCEEDED = "Rate limit exceeded"

# HTTP Status Descriptions
HTTP_200_OK = "OK"
HTTP_201_CREATED = "Created"
HTTP_400_BAD_REQUEST = "Bad Request"
HTTP_401_UNAUTHORIZED = "Unauthorized"
HTTP_403_FORBIDDEN = "Forbidden"
HTTP_404_NOT_FOUND = "Not Found"
HTTP_409_CONFLICT = "Conflict"
HTTP_422_UNPROCESSABLE_ENTITY = "Unprocessable Entity"
HTTP_500_INTERNAL_SERVER_ERROR = "Internal Server Error"
