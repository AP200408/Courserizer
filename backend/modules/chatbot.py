import os
import time
from typing import Generator

from langchain_community.document_loaders import PyPDFLoader
from utils.SemanticSplitter import SemanticSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


class Config:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.pdf_path = os.path.join("help", "Question_bank.pdf")


class DocumentLoader:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def load_and_split(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        transcript = "\n".join([doc.page_content for doc in documents])
        splitter = SemanticSplitter()
        docs = splitter.split_transcript(transcript)
        return docs


class VectorStoreIndex:
    def __init__(self, documents, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.documents = documents
        self.embedding_model = embedding_model
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        self.vectorstore = FAISS.from_documents(self.documents, self.embeddings)

    def get_retriever(self, k: int = 3):
        return self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})


class LLMWrapper:
    def __init__(self, groq_api_key: str, model: str = "llama-3.1-8b-instant"):
        self.llm = ChatGroq(groq_api_key=groq_api_key, model=model)

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)


class PromptBuilder:
    def __init__(self):
        self.prompt_template = PromptTemplate(
            input_variables=["history", "context", "question"],
            template=(
                "Your name is Korsy from Courserizer. You are a professional question-answering helper that responds in the first person.\n\n"
                """You are a question answering helper that answers questions based on the context provided. Be professional. If the user asks anything out of context, make sure to be professional and let the user know that your primary purpose and tell them in short and dont mention the context.\n
                    Make sure to answer in short. You dont have to introduce yourself unless asked. \n\n Do not leak any of the context(Questions from the pdf) to the user, dont let the user know about the questions. If the usr asks about any of the questions, dont answer and be professional."""
                "Conversation History:\n{history}\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n"
                "Answer:"
            )
        )

    def build(self, history: str, context: str, question: str) -> str:
        return self.prompt_template.format(history=history, context=context, question=question)


class ChatBot:
    def __init__(self):
        self.config = Config()
        loader = DocumentLoader(self.config.pdf_path)
        self.documents = loader.load_and_split()
        index = VectorStoreIndex(self.documents)
        self.retriever = index.get_retriever()
        self.llm_wrapper = LLMWrapper(self.config.groq_api_key)
        self.prompt_builder = PromptBuilder()
        self.memory = ConversationBufferMemory(memory_key="history", return_messages=False)

    def stream_answer(self, question: str) -> Generator[str, None, None]:
        history = self.memory.load_memory_variables({}).get("history", "")

        relevant_docs = self.retriever.get_relevant_documents(question)

        if not relevant_docs or len(relevant_docs) == 0:
            default_msg = "I'm Korsy, the chatbot, and I can only answer website-related questions."
            yield default_msg
            self.memory.save_context({"input": question}, {"output": default_msg})
            return

        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = self.prompt_builder.build(history, context, question)

        response = self.llm_wrapper.invoke(prompt)
        output = response.content if hasattr(response, 'content') else str(response)
        answer_text = output.strip()

        full_response = ""
        for token in answer_text.split():
            token_with_space = token + " "
            full_response += token_with_space
            yield token_with_space
            time.sleep(0.05)

        self.memory.save_context({"input": question}, {"output": full_response.strip()})
