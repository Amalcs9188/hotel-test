from mangum import Mangum
from main import app

# Wrap the FastAPI app with Mangum to handle Lambda events
lambda_handler = Mangum(app)
