"""
Used for any globals needed during the program.
Only window entities like root currently. 
Might move the db connection here eventually rather than passing it
around everywhere.
"""


class Globals():
    temp = ""   # for garbage collection
