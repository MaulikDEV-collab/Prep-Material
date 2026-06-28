from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#defining an instance of the FastAPI class, which will be our main application
app = FastAPI()

#via this class we can define the structure of the data that we want to receive in the request body
class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

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


#this is a decorator that tells FastAPI that this function will handle GET requests to the root URL ("/")
@app.get("/")
def root():
    return {"message": "Hello World"}


#this is a decorator that tells FastAPI that this function will handle GET requests to the "/posts" URL
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#this is a decorator that tells FastAPI that this function will handle POST requests to the "/posts" URL
@app.post("/posts")
def create_posts(new_post: Post):
    #.dict() method is used to convert the Pydantic model instance into a dictionary
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 1000000) #this line generates a random integer between 0 and 1,000,000 and assigns it to the 'id' key of the post_dict dictionary
    my_posts.append(post_dict) #this line adds the post_dict to the my_posts list
    return {"data": post_dict} 


#Lets see how to retrieve a specific post by its id using a path parameter. 
@app.get("/posts/{id}")
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







#deleting a post by its id using a path parameter.
@app.delete("/posts/{id}")
def delete_post(id: int):   
    for p in my_posts:
        if p['id'] == int(id):
            my_posts.remove(p) #this line removes the post from the my_posts list
            return Response(status_code=status.HTTP_204_NO_CONTENT) #this line returns a response with a 204 status code, indicating that the request was successful but there is no content to return.
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")



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
           