"""FastAPI Car Shop ERP - Professional ERP System"""

__version__ = "1.0.0"
__author__ = "Development Team"
__email__ = "dev@carshop.com"


def main():
    """Entry point for the application."""
    import uvicorn

    from app.main import app

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")


if __name__ == "__main__":
    main()
