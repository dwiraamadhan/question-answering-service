from fastapi import FastAPI
from api.question_answering import router
from fastapi.middleware.cors import CORSMiddleware
import os, threading, sys
from confluent_kafka import Consumer, KafkaError, KafkaException
from functions.QA import process_answer
from kafka.producer import send_to_kafka


app = FastAPI()

origins = ["http://localhost:5173", os.getenv("WEB_URL")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

def kafka_consumer():
    conf = {
        "bootstrap.servers": os.getenv("BROKER_SERVER"),
        "group.id": os.getenv("GROUP_ID"),
        "auto.offset.reset" : "earliest"
    }

    
    # create consumer instance
    consumer = Consumer(conf)

    # subscribe to topic
    consumer.subscribe([os.getenv("CONSUMER_KAFKA_TOPIC")])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                    (msg.topic(), msg.partition(), msg.offset()))
                    
                elif msg.error():
                    raise KafkaException(msg.error())
                
            else:
                # consumer.commit(asynchronous=False)
                message = msg.value().decode('utf-8')
                print('Received message: %s' % (msg.value().decode('utf-8')))


                response = process_answer(message)
                print(f"Response: {response}")

                send_to_kafka(response)
                print("response sent to kafka")


    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


def start_kafka_consumer():
    consumer_thread = threading.Thread(target=kafka_consumer)
    consumer_thread.start()


if __name__ == "__main__":
    # Start Kafka Consumer in a separate thread
    start_kafka_consumer()

    # Start FastAPI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

