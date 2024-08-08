import uvicorn
from fastapi import FastAPI, HTTPException
from Infrastructure import NotFoundException, ToyModel, ToyPurchaseModel
from ToyBoxQueries import ToyQueryProcessor
from ToyBoxCommands import ToyCommandProcessor
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
    """Adds a new toy to the database using ToyCommandProcessor.
    Parameters:
        - toy (ToyModel): The toy instance to be added.
    Returns:
        - dict: A dictionary with a message key indicating success or failure, and a toy key with the added toy details on success, or payload with the toy details on failure.
    Processing Logic:
        - The function prints a message before and after attempting to add a toy.
        - It utilizes a try-except block to catch exceptions during the toy addition process.
        - On success, a message of "Updated successfully" is returned with the toy instance added.
        - On failure, a message of "Something went wrong" is returned with the original toy data."""
    try:
        print(f"Adding toy to DB")
        new_toy = ToyCommandProcessor.add_toy(toy)
        return {"message": "Updated successfully", "toy": new_toy}
    except Exception as exc:
        print(exc)
    return {"message": "Something went wrong", "payload": toy}


@app.put("/toy", status_code=200)
def buy_toy(toy_purchase: ToyPurchaseModel):
    try:
        response = ToyCommandProcessor.buy_toy(toy_purchase)
        return {"message": "Purchased toy successfully", "response": response}
    except Exception as exc:
        print(exc)
    return {"messaage": "Something went wrong", "payload": toy_purchase}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
