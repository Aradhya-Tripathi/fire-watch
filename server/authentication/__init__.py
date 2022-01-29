from dotenv import load_dotenv
from models.auth_model import AuthModel

from .issue_jwt import AuthToken

load_dotenv()

issue_keys = AuthToken()
auth_model = AuthModel()
