from dotenv import load_dotenv
import os

load_dotenv()
print("KEY =", os.getenv("TOGETHERAI_API_KEY"))