import logging
from agent import create_app
from agent.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("instagram_agent.log"),
        logging.StreamHandler(),
    ],
)

Config.validate()
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
