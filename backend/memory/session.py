"""
Session Memory

Stores conversation history for each session.
"""

from collections import defaultdict
from datetime import datetime
from utils.logger import logger


class SessionMemory:

    def __init__(self):

        self.sessions = defaultdict(list)

        logger.info("Session Memory initialized.")

    # ---------------------------------------------

    def add_message(
            self,
            session_id: str,
            role: str,
            content: str
    ):

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
        )

    # ---------------------------------------------

    def history(
            self,
            session_id: str
    ):

        return self.sessions.get(session_id, [])

    # ---------------------------------------------

    def last_messages(
            self,
            session_id: str,
            limit: int = 10
    ):

        return self.sessions.get(
            session_id,
            []
        )[-limit:]

    # ---------------------------------------------

    def clear(
            self,
            session_id: str
    ):

        if session_id in self.sessions:

            del self.sessions[session_id]

    # ---------------------------------------------

    def all_sessions(self):

        return list(self.sessions.keys())

    # ---------------------------------------------

    def size(
            self,
            session_id: str
    ):

        return len(
            self.sessions.get(
                session_id,
                []
            )
        )