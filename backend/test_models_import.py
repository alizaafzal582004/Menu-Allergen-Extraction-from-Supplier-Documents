from app.models import Document

print("✅ Document model imported successfully!")
print("Table name:", Document.__tablename__)
print("Columns:", [col.name for col in Document.__table__.columns])