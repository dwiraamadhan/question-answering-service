from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# function to access knowledge from vector store
def get_data_from_pinecone():
    # define pinecone api key
    os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

    # create object db to access pinecone
    db = PineconeVectorStore.from_existing_index(
        index_name=os.getenv("PINECONE_INDEX_NAME"),
        embedding=OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    print("db berhasil diinisiasi")
    return db

# function to get response from llm
def qa_llm():
    # create object llm
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_GPT_MODEL"),
        temperature=0.2
    )
    print("llm berhasil diinisiasi")

    # create prompt template
    prompt = ChatPromptTemplate.from_template(
        """
        You are a Customer Service Bank and your job is to greet customers and help them answer questions related to Bank BNI.
            Context: {context}
            Question: {input}
        """
        
    )

    # create chain
    document_chain = create_stuff_documents_chain(
        llm = llm,
        prompt = prompt
    )

    # retrieve data knowledge from pinecone
    retriever = get_data_from_pinecone().as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain

# function to proses question answering
def process_answer(prompt):
    question = prompt
    chain = qa_llm()
    answer = chain.invoke({"input": question})
    response = answer["answer"]
    print("question answering successful")
    return response
    
