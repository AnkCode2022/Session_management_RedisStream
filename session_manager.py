from session_store import SessionStore

store = SessionStore()

session = store.get_session(
    "01JXABCDEF123456789"
)

if session:

    print("\nSession Details")
    print("-" * 50)

    print(session)

    print("\nActive Intent:")
    print(session["active_intent"])

    print("\nIntent Queue:")
    print(session["intent_queue"])

    print("\nIntent Status:")
    print(
        session["intents"]
        ["01JXINTENT001"]
        ["status"]
    )

else:
    print("Session not found")
