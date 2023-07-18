from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                #El tag se utiliza para separación en la documentación
                tags = ['products'],
                responses={404:{"message":"No encontrado"}})

product_list = ["Producto 1", "Producto 2", "Producto 3"]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id: int):
    return product_list[id]