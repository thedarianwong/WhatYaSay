from fastapi import FastAPI
import credential_handler

app = FastAPI() 

credential_handler.request_creds()

@app.get("/")
async def root () : 

    return {"message": "Hello world"}