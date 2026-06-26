from langchain_core.prompts import PromptTemplate
from langchain__openai import OpenAI
from langchain_openai import OpenAIEmbeddings 
from langchain_openai import ChatOpenAI
from langchain_core.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

documents = [Document(page_content="I forgot my password and cannot access my account. How can I reset my password?", metadata={"source": "knowledge_base_article_1"}),
             Document(page_content="To reset your password, click on the 'Forgot Password' link on the login page and follow the instructions sent to your registered email address.", metadata={"source": "knowledge_base_article_2"}),
             Document(page_content="If you are unable to reset your password using the 'Forgot Password' link, please contact our support team for further assistance.", metadata={"source": "knowledge_base_article_3"})]
