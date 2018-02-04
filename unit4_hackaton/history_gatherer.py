import sqlite3


class HistoryGatherer:
    query_str = """
    SELECT p.url FROM moz_historyvisits AS h, moz_places AS p
    WHERE p.id == h.place_id
    ORDER BY h.visit_date
    """

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.already_visited = set()

    def get_urls(self):
        cursor = self.conn.cursor()
        urls = set([row[0] for row in cursor.execute(self.query_str)])
        to_return = urls - self.already_visited
        return list(to_return)

    def cache(self, *urls):
        self.already_visited = self.already_visited | set(urls)
