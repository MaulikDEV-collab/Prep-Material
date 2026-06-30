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
    published: Optional[bool] = True


@app.get("/sqlalchemy")
def test_post(db:Session = Depends(get_db)):
    posts = db.query(model.Post).all() #this will fetch all the data in table
    return {"data" : posts}
#if you look here we are not using any sql query, we are just tapping into the database (db) object and call query then what specific model

@app.get("/posts")
def get_post(db:Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data" : posts}


'''
@app.post("/posts")
def create_post(post: Post, db:Session = Depends(get_db)):
    new_post = model.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post) #we need to add the data to the database using the db object
    db.commit() #like how previously did conn.commit(), we need to commit here also
    db.refresh(new_post) #this is like returning the data which we newly created
    return {"data" : new_post}
    '''
#there is much more efficient way of doing this, if we had more than 50 columns we had to write post.title, post.blabla 50 times, what we can do instead is convert the post object into a dictionary and then unpack the whole dictionary into model.Post()
@app.post("/posts")
def create_post(post: Post, db:Session = Depends(get_db)):
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}




@app.get("/posts/{id}")
def get_post(id : int, db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))#we are converting id into string since in the query its a string we are passing.
    # test_post = cursor.fetchone()
    # conn.commit()
    test_post = db.query(model.Post).filter(model.Post.id == id).first()#this will fetch the first value found
    return {"data": test_post}



#deleting a post in db using cursor
@app.delete("/posts/{id}")
def delete_post(id: int, db:Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(model.Post).filter(model.Post.id == id)
    #here post is a query and not an actual post, since we haven't tapped in using a first() or all()
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    print(delete_post)
    post.delete(synchronize_session=False)
    db.commit()



@app.put("/posts/{id}")
def update_post(id : int, updated_post: Post, db:Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published,str(id)))       
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post_query = db.query(model.Post).filter(model.Post.id == id)
    post = updated_post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")
    
    updated_post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"Post Updated" : updated_post_query.first()}    
