from sqlalchemy import Column, Integer, Date, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class ReporteRendimiento(Base):
    __tablename__ = "reportes_rendimiento"
    id_reporte = Column(Integer, primary_key=True, index=True)
    periodo_inicio = Column(Date, nullable=False)
    periodo_fin = Column(Date, nullable=False)
    total_visitantes = Column(Integer, default=0)
    total_descargas = Column(Integer, default=0)
    total_prospectos = Column(Integer, default=0)
    total_propuestas = Column(Integer, default=0)
    total_ventas = Column(Integer, default=0)
    ingresos_totales = Column(Numeric(14, 2), default=0)
    tasa_conversion_pct = Column(Numeric(5, 2), default=0)
    tasa_cierre_pct = Column(Numeric(5, 2), default=0)
    generado_en = Column(DateTime, default=func.now())
