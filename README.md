# Query Summary

Query Summary is a Flask middleware designed to track MongoDB queries and provide a summary of query statistics. It includes a web interface to display the last 10 requests and their associated query details.


## Usage
Here's an example of how to use the package:

```python
# Import the package
from query_summary import QuerySummaryMiddleware

# Obtain a Redis Cache Manager instance
query_summary_middleware = QuerySummaryMiddleware(app)
```