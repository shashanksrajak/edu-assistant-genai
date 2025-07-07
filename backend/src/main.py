from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.routes.workflow import router as workflow_router
import logging
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

origins = [
    "*",
    "http://localhost:3000",
]

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router, prefix='/api/workflows',
                   tags=['workflows'])


@app.get("/")
def read_root():
    return {"status": "Okay", "message": "Server is Running."}


def main():
    print("Hello from leave-application-agent!")

    uvicorn.run(app, host="0.0.0.0", port=7007)


if __name__ == "__main__":
    main()
