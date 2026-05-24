from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

import models.seller, models.client, models.product, models.campaign
import models.interaction, models.alert, models.followup
import models.proposal, models.sale, models.report

from routers import products, interactions, proposals, sales
from routers import clients, campaigns
from routers import sellers, alerts, followups
from routers import reports, views

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zimbra Transactional System",
    description="Sales and marketing transactional system - Uniminuto 2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(interactions.router)
app.include_router(proposals.router)
app.include_router(sales.router)
app.include_router(clients.router)
app.include_router(campaigns.router)
app.include_router(sellers.router)
app.include_router(alerts.router)
app.include_router(followups.router)
app.include_router(reports.router)
app.include_router(views.router)

@app.get("/")
def root():
    return {"message": "Zimbra API running", "docs": "/docs"}
