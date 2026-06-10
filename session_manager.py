from datetime import datetime
from uuid import uuid4

import redis


class SessionManager:

    SESSION_TTL = 3600
    MAX_MESSAGES = 100

    def __init__(
        self,
        host="localhost",
        port=6379,
        db=0
    ):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def _current_time(self):
        return datetime.utcnow().isoformat()

    def _generate_session_id(self):
        return str(uuid4())

    def save_session(
        self,
        user_id: str,
        message: str
    ):

        stream_key = f"stream:user:{user_id}"

        latest = self.redis_client.xrevrange(
            stream_key,
            count=1
        )

        if latest:
            return latest[0][1]["session_id"]

        session_id = self._generate_session_id()

        self.redis_client.xadd(
            stream_key,
            {
                "session_id": session_id,
                "message": message,
                "created_at": self._current_time()
            }
        )

        self.redis_client.expire(
            stream_key,
            self.SESSION_TTL
        )

        return session_id

    def update_session(
        self,
        user_id: str,
        message: str
    ):

        stream_key = f"stream:user:{user_id}"

        latest = self.redis_client.xrevrange(
            stream_key,
            count=1
        )

        if not latest:
            return self.save_session(
                user_id,
                message
            )

        session_id = latest[0][1]["session_id"]

        self.redis_client.xadd(
            stream_key,
            {
                "session_id": session_id,
                "message": message,
                "created_at": self._current_time()
            }
        )

        self.redis_client.xtrim(
            stream_key,
            maxlen=self.MAX_MESSAGES,
            approximate=True
        )

        self.redis_client.expire(
            stream_key,
            self.SESSION_TTL
        )

        return session_id

    def get_session(
        self,
        user_id: str
    ):

        stream_key = f"stream:user:{user_id}"

        messages = self.redis_client.xrange(
            stream_key,
            min="-",
            max="+"
        )

        if not messages:
            return None

        latest_message = messages[-1][1]

        session_id = latest_message["session_id"]

        last_active_time = latest_message[
            "created_at"
        ]

        history = []

        for msg_id, msg_data in messages:

            history.append(
                {
                    "message_id": msg_id,
                    "message": msg_data["message"],
                    "created_at": msg_data["created_at"]
                }
            )

        return {
            "user_id": user_id,
            "session_id": session_id,
            "last_active_time": last_active_time,
            "message_count": len(history),
            "messages": history
        }
