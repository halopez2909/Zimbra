f = open('zimbra-backend/routers/views.py', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    '''@router.get("/sellers")
def get_sellers_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_seller_performance")).fetchall()
    return [
        {
            "seller_id": row[0],
            "seller_name": row[1],
            "email": row[2],
            "active": row[3],
            "total_alerts": row[4],
            "attended_alerts": row[5],
            "total_followups": row[6],
            "managed_clients": row[7],
            "attention_rate": float(row[8]) if row[8] else 0.0
        }
        for row in rows
    ]''',
    '''@router.get("/sellers")
def get_sellers_view(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT * FROM vw_seller_performance")).fetchall()
    return [
        {
            "seller_id": row[0],
            "seller_name": row[1],
            "total_alerts": row[2],
            "attended_alerts": row[3],
            "total_followups": row[4],
            "attention_rate": float(row[5]) if row[5] else 0.0
        }
        for row in rows
    ]'''
)
f = open('zimbra-backend/routers/views.py', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
