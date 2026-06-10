from pprint import pprint

from session_manager3 import SessionManager

manager = SessionManager()

session = manager.get_session(
    user_id="user_123"
)

pprint(session)
