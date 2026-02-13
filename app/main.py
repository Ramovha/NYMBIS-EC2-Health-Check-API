"""Flask application factory module."""
from flask import Flask
from app.config import DevelopmentConfig
from app.api.routes import health_bp


def create_app(config_class=DevelopmentConfig):
    """Create and configure the Flask application.
    
    Args:
        config_class: Configuration class to use (default: DevelopmentConfig)
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(health_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
