from core.database import Database

db = Database()
articles = db.get_unposted_articles("VIC")
print(f"Found {len(articles)} unposted articles for VIC")
for a in articles[:5]:
    print(f"- {a['title']} ({a['council_id']})")
