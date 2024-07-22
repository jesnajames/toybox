import uvicorn
from fastapi import FastAPI, HTTPException
from Infrastructure import NotFoundException, ToyModel
from Query import ToyQueryProcessor
from Command import ToyCommandProcessor
from SampleResponse import toy_response

app = FastAPI(
    title="My Little ToyBox",
    description="Tired of stepping on Legos and tripping over remote cars? Put them in the ToyBox for another child to play with",
    version="1.0.0")


@app.get("/")
def home():
    return {"message": "Welcome to My Little ToyBox! Sharing with you is fun for me too!"}


@app.get("/toy/{toy_id}", status_code=200, responses=toy_response)
def get_toy(toy_id: str):
    try:
        toy = ToyQueryProcessor.get_toy(toy_id)
    except NotFoundException as nfe:
        raise HTTPException(status_code=nfe.error_code, detail=nfe.error_description)
    return {"message": toy}

@app.post("/toys", status_code=200)
def add_toy(toy: ToyModel):
    try:
        print(f"Adding toy to DB")
        new_toy = ToyCommandProcessor.add_toy(toy)
        return {"message": "Updated successfully", "toy": new_toy}
    except Exception as exc:
        print(exc)
    return {"message": "Something went wrong"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)