# SQLAlchemy instance created without app to allow for flexible initialization
db = SQLAlchemy()

# Default image URL defined as constant to maintain consistency across the application
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    """Site user."""
    
    # Explicitly name the table for clarity and control
    __tablename__ = "users"

    # Primary key auto-increments by default in PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    
    # Text fields chosen over String for unlimited length
    # nullable=False ensures we always have basic user information
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    
    # Default image provided if none specified
    # nullable=False with default ensures we always have an image
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user."""
        # Property decorator allows method to be called like an attribute
        # f-string used for efficient string formatting
        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect this database to provided Flask app."""
    # Two-step initialization pattern:
    # 1. Set db.app for compatibility with some extensions
    # 2. Call init_app() for proper Flask application factory pattern
    db.app = app
    db.init_app(app) 