from pymongo.monitoring import CommandListener
import json
from collections import defaultdict, deque

class QueryCounter(CommandListener):
    """A MongoDB CommandListener to count and log database queries."""

    def __init__(self):
        self.reset()
        self.last_ten_requests = deque(maxlen=10)  # Store the last 10 requests

    def reset(self):
        """Resets the query count and details."""
        self._queries = defaultdict(int)

    def started(self, event):
        """Called when a command starts."""
        try:
            query_str = json.dumps(
                {"command_name": event.command_name, "command": event.command},
                sort_keys=True,
                default=str,
            )
            self._queries[query_str] += 1
        except Exception:
            pass

    def succeeded(self, event):
        """Called when a command succeeds."""
        pass

    def failed(self, event):
        """Called when a command fails."""
        pass

    @property
    def total_queries(self):
        """Returns the total number of queries."""
        return sum(self._queries.values())

    @property
    def repeated_queries(self):
        """Returns queries that were executed more than once."""
        return {k: v for k, v in self._queries.items() if v > 1}

    def summary(self):
        """Returns a summary of the queries."""
        return {
            "total_queries": self.total_queries,
            "repeated_query_count": sum(v for v in self.repeated_queries.values()),
            "repeated_queries": self.repeated_queries,
        }

    def add_request_summary(self, request_url, request_method, query_summary):
        """Adds a request summary to the last_ten_requests."""
        self.last_ten_requests.append({
            "url": request_url,
            "method": request_method,
            "query_summary": query_summary,
        })
        # Reset the query counter if the deque reaches its maximum length
        if len(self.last_ten_requests) == self.last_ten_requests.maxlen:
            self.reset()

    def get_last_ten_requests(self):
        """Returns the last ten request summaries."""
        return list(self.last_ten_requests)