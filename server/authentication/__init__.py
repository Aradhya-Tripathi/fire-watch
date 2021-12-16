from dotenv import load_dotenv
from models.auth_model import AuthModel

from .issue_jwt import TokenAuth

load_dotenv()

issue_keys = TokenAuth()
auth_model = AuthModel()
