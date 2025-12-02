from dateutil import parser as date_parser

dates = [
    "News/ Nov 21, 2025",
    "News / Nov 21, 2025",
    "Media Release - 21 November 2025",
    "21 Nov 2025 - Council Meeting",
    "Budget 2025 adopted on Nov 21 2024"
]

for d in dates:
    try:
        dt = date_parser.parse(d, dayfirst=True, fuzzy=True)
        print(f"'{d}' -> {dt}")
    except Exception as e:
        print(f"'{d}' -> Error: {e}")
