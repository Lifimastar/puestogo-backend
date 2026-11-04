import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.db.session import get_session
from src.models import Merchant, Product, Order, OrderItem
from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int

class OrderCreate(BaseModel):
    merchant_id: uuid.UUID
    items: list[OrderItemCreate]

app = FastAPI(title="PuestoGo API", version="0.1.0")

# Permitir peticiones desde Flutter (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "PuestoGo"}

# Endpoint que consumirá la pantalla de "Restaurants" de tu imagen
@app.get("/merchants")
async def get_merchants(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Merchant))
    merchants = result.scalars().all()
    return merchants

@app.get("/merchants/{merchant_id}/products")
async def get_products(merchant_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Product).where(Product.merchant_id == merchant_id)
    )
    return result.scalars().all()

@app.post("/orders")
async def create_order(order_data: OrderCreate, session: AsyncSession = Depends(get_session)):
    # 1. Calcular el total en el servidor (NUNCA confiar en el precio del cliente)
    total = 0.0
    db_items = []
    for item in order_data.items:
        product = await session.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        total += product.price * item.quantity
        db_items.append({"product_id": product.id, "quantity": item.quantity, "price": product.price})

    # 2. Crear la orden (usando flush para obtener el ID)
    new_order = Order(merchant_id=order_data.merchant_id, total=total)
    session.add(new_order)
    await session.flush() # Obtiene el ID de la orden sin hacer commit

    # 3. Crear los ítems de la orden
    for item_data in db_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price=item_data["price"]
        )
        session.add(order_item)

    # 4. Confirmar la transacción
    await session.commit()
    await session.refresh(new_order)
    
    return {"order_id": new_order.id, "total": new_order.total, "status": new_order.status}