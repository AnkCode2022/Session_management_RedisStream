from session_manager3 import SessionManager

manager = SessionManager()

session_id = manager.update_session(
    user_id="user_123",
    message="Tell me about Redis Streams"
)

print("Session Updated")
print("Session ID:", session_id)
