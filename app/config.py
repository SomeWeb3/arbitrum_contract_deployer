import os

import dotenv

dotenv.load_dotenv()

ARBITRUM_URL: str = os.environ["ARBITRUM_URL"]
AMOUNT_LOW: float = float(os.environ["AMOUNT_LOW"])
AMOUNT_HIGH: float = float(os.environ["AMOUNT_HIGH"])
