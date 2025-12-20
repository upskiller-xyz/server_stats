import os
from typing import Dict, Any

# Disable GPU/CUDA to prevent bus errors on WSL2
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['OMP_NUM_THREADS'] = '1'

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.server.flask_server import ServerMetricsApp, FlaskServerConfig


def main() -> None:
    """Main entry point"""
    port = int(os.getenv("PORT", 8081))
    config = FlaskServerConfig(
        host="0.0.0.0",
        port=port,
        debug=True
    )
    server = ServerMetricsApp(config)
    server.run()


# Create app instance for gunicorn only when needed
# Don't create at module import time to avoid bus errors
def create_app():
    """Factory function for creating the Flask app (for gunicorn)"""
    port = int(os.getenv("PORT", 8081))
    config = FlaskServerConfig(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    server = ServerMetricsApp(config)
    return server.app


# Only create app instance if not running as main (i.e., when imported by gunicorn)
if __name__ != "__main__":
    app = create_app()
else:
    # Running as main script
    main()