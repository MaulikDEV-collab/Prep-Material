from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model
from .database import engine, get_db
from sqlalchemy.orm import Session
'''this is a copy that i have created in order to understand ORM.
'''
#for orm
model.Base.metadata.create_all(bind=engine)

#defining an instance of the FastAPI class, which will be our main application
app = FastAPI()

'''
A session object is kind of what's responsible for talking with our database and so we created this function
where we actually get a connection/session to our database. And so, everytime we get a session we are going to 
be able to send a SQL. We can keep calling this function everytime we get a request to any of our API endpoints

'''


#via this class we can define the structure of the data that we want to receive in the request body
class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: Optional[bool] = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Laxmi@2811', cursor_factory=RealDictCursor)
    #RealDictCursor will give you the column name as well as the value when querying data.
        cursor = conn.cursor() #to execute the sql statements we will use this cursor
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error ",error)
        time.sleep(3)


#this is a list that we have defined to store our posts data, it contains two dictionaries representing two posts with their title, content and id
my_posts = [{"title": "post 1", "content": "content of post 1", "id": 1}, {"title": "post 2", "content": "content of post 2", "id": 2}]


@app.get("/sqlalchemy")
def test_post(db:Session = Depends(get_db)):
    posts = db.query(model.Post).all() #this will fetch all the data in table
    return {"data" : posts}
#if you look here we are not using any sql query, we are just tapping into the database (db) object and call query then what specific model


#create_posts for crud with database
@app.post("/posts")
def create_posts(new_post: Post):
    try:
        cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''', (new_post.title, new_post.content, new_post.published))
        #in order to get the value returned we have to fetch it
        post_created = cursor.fetchone()
        conn.commit()
        return {"data": post_created}
    except Exception as e:
        conn.rollback()
        print("POST /posts failed:", repr(e))
        raise HTTPException(status_code=500, detail="Insert failed") 
#here %s represents the variable (title and etc.) which needs to be passed. the order matters.


#Lets see how to retrieve a specific post by its id using a path parameter. 
'''@app.get("/posts/{id}")
def get_post(id : int, response: Response):  #you can either specify the type of parameter expected like here int or you can convert it later to int type below
    #this line uses a list comprehension to iterate through the my_posts list and find the post with the matching id. If found, it returns the post; otherwise, it returns None.
    for p in my_posts:
        #anytime we have a path parameter, its always going to be a string, so we need to convert it to an integer before comparing it with the id of the post.
        if p['id'] == int(id):
            return {"post_detail": p}
    
    # response.status_code = 404 #this line sets the status code of the response to 404, indicating that the requested resource was not found.    
    # return {"detail": f"Post with id {id} was not found"}        
    #you could do the above two lines or you could use the below line to raise an HTTPException with a 404 status code and a custom detail message. This is a more concise way to handle the case when the post is not found.
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
'''
@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))#we are converting id into string since in the query its a string we are passing.
    test_post = cursor.fetchone()
    conn.commit()
    return {"data": test_post}



'''
#deleting a post by its id using a path parameter.
@app.delete("/posts/{id}")
def delete_post(id: int):   
    for p in my_posts:
        if p['id'] == int(id):
            my_posts.remove(p) #this line removes the post from the my_posts list
            return Response(status_code=status.HTTP_204_NO_CONTENT) #this line returns a response with a 204 status code, indicating that the request was successful but there is no content to return.
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
'''

#deleting a post in db using cursor
@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    print(delete_post)
    return {"deleted_post" : deleted_post}

'''
#updating a post by its id using a path parameter.
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #here we are using the same logic used in create_post since we expect values here as well.
    post_dict = post.dict() 
    for p in my_posts:
        if p['id'] == int(id):
            post_dict['id'] = p['id'] 
            my_posts[my_posts.index(p)] = post_dict #this line updates the post in the my_posts list with the new data from post_dict
            return {"data": post_dict}
 '''

@app.put("/posts/{id}")
def update_post(id : int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published,str(id)))       
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    return {"Post Updated" : updated_post}    
