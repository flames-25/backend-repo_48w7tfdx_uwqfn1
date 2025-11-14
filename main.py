import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from database import db, create_document, get_documents
from schemas import Tour, Booking, Inquiry

app = FastAPI(title="Tour Service API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Tour Service API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Welcome to the Tour Service API"}

# Utility to ensure collections exist (Mongo is schemaless, but this helps logical grouping)

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# -------- Public content endpoints --------

@app.get("/api/tours", response_model=List[Tour])
async def list_tours(limit: int = 20) -> List[Tour]:
    docs = await get_documents("tour", {}, limit)
    # Fallback sample data if DB empty
    if not docs:
        sample = [
            {
                "title": "Explore Bali Paradise",
                "description": "Paket liburan 4 hari 3 malam mencakup Ubud, Kintamani, dan Pantai Pandawa.",
                "price": 299.0,
                "duration_days": 4,
                "location": "Bali, Indonesia",
                "image_url": "https://images.unsplash.com/photo-1542978708-6f1a7a7f33f3",
                "highlights": ["Ubud rice terrace", "Mount Batur sunrise", "Beach hopping"],
                "rating": 4.9,
            },
            {
                "title": "Magelang & Borobudur Escape",
                "description": "2 hari menikmati sunrise di Borobudur dan kuliner lokal.",
                "price": 159.0,
                "duration_days": 2,
                "location": "Yogyakarta, Indonesia",
                "image_url": "https://images.unsplash.com/photo-1541417904950-b855846fe074",
                "highlights": ["Borobudur sunrise", "Malioboro tour"],
                "rating": 4.7,
            },
        ]
        return [Tour(**t) for t in sample]
    return [Tour(**d) for d in docs]

class BookingResponse(BaseModel):
    status: str
    booking_id: Optional[str] = None

@app.post("/api/book", response_model=BookingResponse)
async def create_booking(payload: Booking) -> BookingResponse:
    try:
        doc_id = await create_document("booking", payload.model_dump())
        return BookingResponse(status="success", booking_id=str(doc_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inquiry")
async def send_inquiry(payload: Inquiry) -> Dict[str, Any]:
    try:
        await create_document("inquiry", payload.model_dump())
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
