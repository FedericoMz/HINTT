from tools.drawer import Drawer
from tools.logger import logger

if __name__ == "__main__":
    logger.info("App starting...")
    app = Drawer()
    app.run()
