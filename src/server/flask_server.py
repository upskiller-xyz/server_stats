from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Tuple, Dict, Any
from src.server.constants import (
    ServerConfig,
    HttpStatusCode,
    RouteEndpoints,
    ResponseKeys
)
from src.server.validator import RequestValidator, ValidationError
from src.server.metric_calculator import MetricCalculator
from src.server.models import RunRequest, RunResponse, ErrorResponse


class FlaskServerConfig:
    """Configuration class for Flask server."""

    def __init__(
        self,
        host: str = ServerConfig.DEFAULT_HOST.value,
        port: int = ServerConfig.DEFAULT_PORT.value,
        debug: bool = False
    ):
        """
        Initialize server configuration.

        Args:
            host: Server host address
            port: Server port number
            debug: Enable debug mode
        """
        self.host = host
        self.port = port
        self.debug = debug


class ServerMetricsApp:
    """
    Main Flask server application for metrics calculation.
    Encapsulates server setup and route handling.
    """

    def __init__(self, config: FlaskServerConfig):
        """
        Initialize Flask server with configuration.

        Args:
            config: Server configuration object
        """
        self._config = config
        self._app = Flask(__name__)
        self._setup_cors()
        self._setup_logging()
        self._validator = RequestValidator()
        self._calculator = MetricCalculator()
        self._register_routes()

    def _setup_cors(self) -> None:
        """Configure CORS for the Flask application."""
        CORS(self._app)

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO if not self._config.debug else logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._logger = logging.getLogger(__name__)

    def _register_routes(self) -> None:
        """Register all API routes."""
        self._app.route(RouteEndpoints.RUN.value, methods=['POST'])(self._handle_run)
        self._app.route(RouteEndpoints.HEALTH.value, methods=['GET'])(self._handle_health)

    def _handle_run(self) -> Tuple[Dict[str, Any], int]:
        """
        Handle POST /run endpoint.

        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            data = request.get_json()
            if data is None:
                return self._error_response("Request body must be JSON", HttpStatusCode.BAD_REQUEST.value)

            # Validate request
            self._validator.validate(data)

            # Parse request
            run_request = RunRequest.from_dict(data)

            # Calculate metrics
            metrics = self._calculator.calculate_all(run_request.result, run_request.mask)

            # Build response
            response = RunResponse(metrics=metrics)

            self._logger.info(f"Successfully calculated {len(metrics)} metrics")
            return response.to_dict(), HttpStatusCode.OK.value

        except ValidationError as e:
            self._logger.warning(f"Validation error: {str(e)}")
            return self._error_response(str(e), HttpStatusCode.BAD_REQUEST.value)

        except Exception as e:
            self._logger.error(f"Internal server error: {str(e)}", exc_info=True)
            return self._error_response(
                "Internal server error",
                HttpStatusCode.INTERNAL_SERVER_ERROR.value
            )

    def _handle_health(self) -> Tuple[Dict[str, str], int]:
        """
        Handle GET /health endpoint.

        Returns:
            Tuple of (response_dict, status_code)
        """
        return {ResponseKeys.STATUS.value: "healthy"}, HttpStatusCode.OK.value

    def _error_response(self, message: str, status_code: int) -> Tuple[Dict[str, str], int]:
        """
        Create error response.

        Args:
            message: Error message
            status_code: HTTP status code

        Returns:
            Tuple of (error_dict, status_code)
        """
        response = ErrorResponse(error=message)
        return response.to_dict(), status_code

    def run(self) -> None:
        """Start the Flask server."""
        self._logger.info(f"Starting server on {self._config.host}:{self._config.port}")
        self._app.run(
            host=self._config.host,
            port=self._config.port,
            debug=self._config.debug
        )

    @property
    def app(self) -> Flask:
        """
        Get the underlying Flask app instance.

        Returns:
            Flask application instance
        """
        return self._app
