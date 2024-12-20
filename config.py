import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in environment variables.")