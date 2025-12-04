from dateutil import parser

dates = [
    "3rd December 2025",
    "2nd December 2025",
    "19th November 2025",
    "1st October 2025"
]

for d in dates:
    try:
        dt = parser.parse(d, fuzzy=True)
        print(f"'{d}' -> {dt}")
    except Exception as e:
        print(f"'{d}' -> Error: {e}")
