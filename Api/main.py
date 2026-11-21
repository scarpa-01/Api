from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Minha API", version="1.0.0")


# ---------- Modelo de exemplo ----------
class Item(BaseModel):
    nome: str
    quantidade: int = 1


# ---------- "Base de dados" em memória ----------
itens_db: dict[int, Item] = {}
proximo_id = 1


# ---------- Rotas ----------
@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "API a funcionar!"}


@app.get("/itens")
def listar_itens():
    return itens_db


@app.post("/itens")
def criar_item(item: Item):
    global proximo_id
    itens_db[proximo_id] = item
    proximo_id += 1
    return {"id": proximo_id - 1, **item.dict()}


@app.get("/itens/{item_id}")
def obter_item(item_id: int):
    if item_id not in itens_db:
        return {"erro": "Item não encontrado"}
    return itens_db[item_id]


@app.delete("/itens/{item_id}")
def apagar_item(item_id: int):
    if item_id in itens_db:
        del itens_db[item_id]
        return {"mensagem": "Apagado"}
    return {"erro": "Item não encontrado"}

    from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # em produção mete o domínio do teu site
    allow_methods=["*"],
    allow_headers=["*"],
)