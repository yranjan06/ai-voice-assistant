from datetime import datetime

class SessionMemory:
    def __init__(self, max_turns=10):
        self._history = []
        self.max_turns = max_turns

    def add(self, user_text, intent, result):
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "intent": intent,
            "result": str(result.get("output", "done"))[:200],
        })
        # keep only last N turns
        self._history = self._history[-self.max_turns:]

    def get_context(self):
        if not self._history:
            return ""
        lines = ["Recent conversation:"]
        for t in self._history[-3:]:
            lines.append(f'- "{t["user"]}" -> {t["intent"]}')
        return "\n".join(lines)

    def get_all(self):
        return list(self._history)