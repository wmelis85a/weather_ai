import unicodedata

def filter_alerts_by_string(response: dict, query: str) -> dict:
    query = query.lower()

    def alert_matches(alert: dict) -> bool:
        for value in alert.values():
            # string key
            if isinstance(value, str):
                if query in normalize(value):
                    return True

            # list key (e.g., instructions, regions, etc)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and query in normalize(item):
                        return True

        return False

    return {
        "hoje": [a for a in response.get("hoje", []) if alert_matches(a)],
        "futuro": [a for a in response.get("futuro", []) if alert_matches(a)],
    }


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKD", text)\
        .encode("ascii", "ignore")\
        .decode("ascii")\
        .lower()
