import logging
import sys

def setup_logger():
    logger = logging.getLogger("trading_bot")
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)

    # Console Handler (Optional for CLI info, set to WARNING so it is less noisy)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)

    # File Handler
    file_handler = logging.FileHandler("trading_bot.log")
    file_handler.setLevel(logging.INFO)

    file_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
    )
    
    console_handler.setFormatter(file_format)
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
