"""
Server Stats Application Entry Point

This module serves as the entry point for the Server Stats application.
It initializes and starts the Flask server with proper configuration.
"""
from src.server.flask_server import ServerMetricsApp, FlaskServerConfig


def main() -> None:
    """
    Main entry point for the application.
    Creates and runs the Flask server with default configuration.
    """
    config = FlaskServerConfig(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

    server = ServerMetricsApp(config)
    server.run()


if __name__ == "__main__":
    main()
