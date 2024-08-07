from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.questions import QuestionClass
from functions.QA import process_answer
from datetime import datetime
from config.database import collection
from kafka.producer import send_to_kafka
from functions.check_health_and_readiness import check_db_connection, check_kafka_connection

router = APIRouter()

@router.post("/question")
async def question_answering(question: QuestionClass):
    try:
        # process questions
        response = process_answer(question.text)
        print(f"Question: {question.text}")

        # save question to database
        question_doc = {"text": question.text, "createdAt": datetime.now()}
        question_data = collection.insert_one(question_doc)
        inserted_id = str(question_data.inserted_id)
        print("question data saved")

        # send message to kafka
        send_to_kafka(response)

        return{
            "answer": response,
            "question_saved": {
                "question_id" : inserted_id,
                "question_text" : question.text,
                "createdAt": datetime.now()
            }
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    

@router.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})

# check readiness
@router.get("/ready")
async def readiness_check():
    # check connection to mongoDB
    isReady = check_db_connection() and check_kafka_connection()
    if isReady:
        return JSONResponse(status_code=200, content={"status": "ready"})
    else:
        return JSONResponse(status_code=503, content={"status": "not ready"})