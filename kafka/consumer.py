# import sys, os
# from functions.QA import process_answer
# from confluent_kafka import Consumer, KafkaError, KafkaException
# from kafka.producer import send_to_kafka

# def kafka_consumer():
#     # kafka configuration
#     conf = {
#         "bootstrap.servers": os.getenv("BROKER_SERVER"),
#         "group.id": os.getenv("GROUP_ID"),
#         "auto.offset.reset" : "earliest"
#     }

#     # create consumer instance
#     consumer = Consumer(conf)

#     # subscribe to topic
#     consumer.subscribe([os.getenv("CONSUMER_KAFKA_TOPIC")])

#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 continue

#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     # End of partition event
#                     sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
#                                     (msg.topic(), msg.partition(), msg.offset()))
                    
#                 elif msg.error():
#                     raise KafkaException(msg.error())
                
#             else:
#                 # consumer.commit(asynchronous=False)
#                 message = msg.value().decode('utf-8')
#                 print('Received message: %s' % (msg.value().decode('utf-8')))


#                 response = process_answer(message)
#                 print(f"Response: {response}")

#                 send_to_kafka(response)
#                 print("response sent to kafka")


#     except KeyboardInterrupt:
#         pass

#     finally:
#         consumer.close()





# # # kafka configuration
# # conf = {
# #     "bootstrap.servers": "localhost:9092",
# #     "group.id": "question-answering",
# #     "auto.offset.reset" : "earliest"
# # }

# # # Create customer instance
# # consumer = Consumer(conf)

# # # subscribe to topic
# # consumer.subscribe(["topicPertama"])

# # # Consumer loop
# # try:
# #     while True:
# #         msg = consumer.poll(1.0)
# #         if msg is None:
# #             continue

# #         if msg.error():
# #             if msg.error().code() == KafkaError._PARTITION_EOF:
# #                 # End of partition event
# #                 sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
# #                                 (msg.topic(), msg.partition(), msg.offset()))
# #             elif msg.error():
# #                 raise KafkaException(msg.error())
            
# #         else:
# #             print('Received message: %s' % (msg.value().decode('utf-8')))
# #             consumer.commit(asynchronous=False)

# # except KeyboardInterrupt:
# #     pass

# # finally:
# #     # Close down the consumer to commit final offsets.
# #     consumer.close()

