"""
SQLite functions:

commonly needed SQLite functions I use
"""


def BasicDbQuery(conn, query):
    """Runs SQL query on connection and returns results as list.
    list[0] = list of headings
    list[1] = list(column) of lists(rows) of data"""
    with conn:
        c = conn.cursor()
        c.execute(query)
        query_info = []
        query_info.append([desc[0] for desc in c.description])
        query_info.append(c.fetchall())
        return query_info


def AdvDbQuery(conn, query, dictionary, returnlist=True):
    """Runs SQL query on connection and returns results as list.
    list[0] = list of headings
    list[1] = list(column) of lists(rows) of data"""
    with conn:
        c = conn.cursor()
        c.execute(query, dictionary)
        if returnlist:
            query_info = []
            query_info.append([desc[0] for desc in c.description])
            query_info.append(c.fetchall())
            return query_info
        else:
            return
