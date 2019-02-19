# import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

current_year = datetime.now().year
current_month = datetime.now().strftime("%m")
current_day = datetime.now().strftime("%d")

year_list = [1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930,
             1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942,
             1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954,
             1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966,
             1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978,
             1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
             1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
             2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026,
             2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038,
             2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050]
month_list = ["Jan", "Feb",  "Mar",  "Apr",  "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec",  "Jan"]
day_list_30 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
               12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
               23, 24, 25, 26, 27, 28, 29, 30, 31]


class DateEntry():
    def __init__(self, master):
        self.master = master
        self._build_widgets()
    
    def _build_widgets(self):
        self.date_text = ttk.Label(self.master, state="readonly", text="Date: ")
        self.year = ttk.Combobox(self.master, values=year_list, width="4")
        self.year.set(current_year)
        self.month = ttk.Combobox(self.master, values=month_list, width="3")
        self.day = ttk.Combobox(self.master, values=day_list, width="2")
    
    def pack(self):
        self.date_text.pack(side="left", anchor="n")
        self.year.pack(side="left", anchor="n")