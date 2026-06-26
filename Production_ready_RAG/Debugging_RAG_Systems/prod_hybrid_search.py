from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()


#documents with both semantic and keyword search capabilities
documents = [
    Document(
        page_content="""
        Employees reported being unable to connect to the corporate VPN after a security patch deployment.
        Users experienced authentication failures despite using correct credentials.
        The networking team rolled back the update and restored access.
        """,
        metadata={
            "doc_id": "INC-2024-001",
            "category": "network",
            "title": "VPN Access Failure"
        }
    ),

    Document(
        page_content="""
        Several departments observed delayed email delivery.
        Messages remained queued for extended periods before reaching recipients.
        Investigation revealed a mail server performance bottleneck.
        """,
        metadata={
            "doc_id": "INC-2024-002",
            "category": "email",
            "title": "Email Delivery Delay"
        }
    ),

    Document(
        page_content="""
        Customers were unable to sign in to the online banking portal.
        Users received timeout errors after entering credentials.
        The root cause was database connection pool exhaustion.
        """,
        metadata={
            "doc_id": "SR-87421",
            "category": "banking",
            "title": "Customer Login Issue"
        }
    ),

    Document(
        page_content="""
        Employee EMP-5628 received a replacement laptop after repeated SSD failures.
        The device experienced frequent crashes and unexpected shutdowns.
        A new workstation was issued by the IT department.
        """,
        metadata={
            "doc_id": "EMP-5628",
            "category": "hardware",
            "title": "Employee Laptop Replacement"
        }
    ),

    Document(
        page_content="""
        Invoice INV-2024-9834 was generated for the procurement of networking equipment.
        The shipment included switches, routers, and firewall appliances.
        Payment was approved by the finance department.
        """,
        metadata={
            "doc_id": "INV-2024-9834",
            "category": "finance",
            "title": "Procurement Invoice"
        }
    ),

    Document(
        page_content="""
        Product PRD-A1001 is an ergonomic wireless mouse designed for office productivity.
        Features include adjustable DPI settings, silent clicks, and long battery life.
        """,
        metadata={
            "doc_id": "PRD-A1001",
            "category": "product",
            "title": "Wireless Mouse"
        }
    ),

    Document(
        page_content="""
        Users complained that the HR management application was extremely slow.
        Pages required over 30 seconds to load and search operations frequently timed out.
        Database indexing issues were identified during troubleshooting.
        """,
        metadata={
            "doc_id": "TKT-44192",
            "category": "performance",
            "title": "Slow Application Performance"
        }
    ),

    Document(
        page_content="""
        This knowledge base article explains how users can regain access after forgetting their password.
        The process includes identity verification and secure password reset steps.
        """,
        metadata={
            "doc_id": "KB-1007",
            "category": "knowledge_base",
            "title": "Password Reset Procedure"
        }
    ),

    Document(
        page_content="""
        Order ORD-77881 experienced shipping delays because of severe weather conditions.
        Customers were notified and provided revised delivery timelines.
        """,
        metadata={
            "doc_id": "ORD-77881",
            "category": "logistics",
            "title": "Delayed Product Shipment"
        }
    ),

    Document(
        page_content="""
        The application search feature occasionally returns incorrect results.
        Users reported that searching for customer accounts sometimes displays unrelated records.
        Engineers suspect an indexing inconsistency.
        """,
        metadata={
            "doc_id": "BUG-2194",
            "category": "bug",
            "title": "Search Function Returns Incorrect Results"
        }
    )]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore=Chroma.from_documents(documents, embedding=embeddings, collection_name="hybrid_test")

#create vector retriever for semantic search
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})#return top 3

#BM25 retriever for keyword search
bm25_retriever = BM25Retriever.from_documents(documents, k=2) #return top 2

#Ensemble retriever to combine both semantic and keyword search results
ensemble_retriever = EnsembleRetriever(retrievers=[vector_retriever, bm25_retriever], weights=[0.5, 0.5])#equal weights to both retrievers

#Example query
def test_query(query, name, retriever):
    '''Test a query and show results'''
    # use the public Runnable interface (`invoke` / `ainvoke`) for retrievers
    try:
        # sync invoke is the standard entrypoint for retrievers
        results = retriever.invoke(query)
    except Exception:
        # fallback: if this is a vectorstore-backed retriever, call the underlying vectorstore
        try:
            k = getattr(retriever, 'search_kwargs', {}).get('k', 3) or 3
            results = retriever.vectorstore.similarity_search(query, k=k)
        except Exception:
            # last resort: return empty list
            results = []
    print(f'\n{name} - Query: "{query}"')
    for i, doc in enumerate(results[:3]):
        preview = doc.page_content[:80] + '...'
        print(f' {i+1}. {preview}')
    return results

#test queries
queries = [
    "I forgot my password and cannot access my account",  # Semantic -> KB-1007
    "online banking login timeout",                      # Semantic -> SR-87421
    "EMP-5628",                                          # Keyword -> Employee Laptop
    "INV-2024-9834",                                     # Keyword -> Invoice
    "employee EMP-5628 laptop crash",                    # Hybrid
    "ticket TKT-44192 application slow",                 # Hybrid
]

for query in queries:
    vector_results = test_query(query, "VECTOR", vector_retriever)

    bm25_results = test_query(query, "BM25", bm25_retriever)

    hybrid_results = test_query(query, "HYBRID", ensemble_retriever)

#OUTPUT
# VECTOR - Query: "I forgot my password and cannot access my account"
#  1. 
#         This knowledge base article explains how users can regain access after ...
#  2. 
#         Customers were unable to sign in to the online banking portal.
#         ...
#  3. 
#         Employees reported being unable to connect to the corporate VPN after a...

# BM25 - Query: "I forgot my password and cannot access my account"
#  1. 
#         This knowledge base article explains how users can regain access after ...
#  2. 
#         Order ORD-77881 experienced shipping delays because of severe weather c...

# HYBRID - Query: "I forgot my password and cannot access my account"
#  1. 
#         This knowledge base article explains how users can regain access after ...
#  2. 
#         Customers were unable to sign in to the online banking portal.
#         ...
#  3. 
#         Order ORD-77881 experienced shipping delays because of severe weather c...

# VECTOR - Query: "online banking login timeout"
#  1. 
#         Customers were unable to sign in to the online banking portal.
#         ...
#  2. 
#         Users complained that the HR management application was extremely slow....
#  3. 
#         Employees reported being unable to connect to the corporate VPN after a...

# BM25 - Query: "online banking login timeout"
#  1. 
#         Customers were unable to sign in to the online banking portal.
#         ...
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...

# HYBRID - Query: "online banking login timeout"
#  1. 
#         Customers were unable to sign in to the online banking portal.
#         ...
#  2. 
#         Users complained that the HR management application was extremely slow....
#  3. 
#         The application search feature occasionally returns incorrect results.
# ...

# VECTOR - Query: "EMP-5628"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         Invoice INV-2024-9834 was generated for the procurement of networking e...
#  3. 
#         Product PRD-A1001 is an ergonomic wireless mouse designed for office pr...

# BM25 - Query: "EMP-5628"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...

# HYBRID - Query: "EMP-5628"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         Invoice INV-2024-9834 was generated for the procurement of networking e...
#  3. 
#         The application search feature occasionally returns incorrect results.
# ...

# VECTOR - Query: "INV-2024-9834"
#  1. 
#         Invoice INV-2024-9834 was generated for the procurement of networking e...
#  2. 
#         Order ORD-77881 experienced shipping delays because of severe weather c...
#  3. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...

# BM25 - Query: "INV-2024-9834"
#  1. 
#         Invoice INV-2024-9834 was generated for the procurement of networking e...
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...

# HYBRID - Query: "INV-2024-9834"
#  1. 
#         Invoice INV-2024-9834 was generated for the procurement of networking e...
#  2. 
#         Order ORD-77881 experienced shipping delays because of severe weather c...
#  3. 
#         The application search feature occasionally returns incorrect results.
# ...

# VECTOR - Query: "employee EMP-5628 laptop crash"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         Employees reported being unable to connect to the corporate VPN after a...
#  3. 
#         Users complained that the HR management application was extremely slow....

# BM25 - Query: "employee EMP-5628 laptop crash"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...

# HYBRID - Query: "employee EMP-5628 laptop crash"
#  1. 
#         Employee EMP-5628 received a replacement laptop after repeated SSD fail...
#  2. 
#         Employees reported being unable to connect to the corporate VPN after a...
#  3. 
#         The application search feature occasionally returns incorrect results.
# ...

# VECTOR - Query: "ticket TKT-44192 application slow"
#  1. 
#         Users complained that the HR management application was extremely slow....
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...
#  3. 
#         Several departments observed delayed email delivery.
#         Messages r...

# BM25 - Query: "ticket TKT-44192 application slow"
#  1. 
#         The application search feature occasionally returns incorrect results.
# ...
#  2. 
#         Users complained that the HR management application was extremely slow....

# HYBRID - Query: "ticket TKT-44192 application slow"
#  1. 
#         Users complained that the HR management application was extremely slow....
#  2. 
#         The application search feature occasionally returns incorrect results.
# ...
#  3. 
#         Several departments observed delayed email delivery.
#         Messages r...