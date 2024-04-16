from fastapi import APIRouter, HTTPException
from models.questions import QuestionClass
from functions.QA import process_answer
from datetime import datetime
from config.database import collection

router = APIRouter()

@router.post("/question")
async def question_answering(question: QuestionClass):
    try:
        # process questions
        response = process_answer(question.text)

        # save question to database
        question_doc = {"text": question.text, "createdAt": datetime.now()}
        question_data = collection.insert_one(question_doc)
        inserted_id = str(question_data.inserted_id)
        print("question data saved")

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