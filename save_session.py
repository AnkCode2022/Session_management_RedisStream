from session_manager3 import SessionManager

manager = SessionManager()

session_id = manager.save_session(
    user_id="user_123",
    message="Hello Agent"
)

print("Session Created")
print("Session ID:", session_id)
