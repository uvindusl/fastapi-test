from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts", # + id
    tags=['Posts']
)

@router.get("/",response_model=List[schema.Post])
def get_posts(db:Session = Depends(get_db), current_user:int  =  Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db:Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,100000000)
    # my_posts.routerend(post_dict)
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}",response_model=schema.Post)
def get_posts(id: int, db:Session = Depends(get_db), current_user:int  =  Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with {id} was not found"}
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,  db:Session = Depends(get_db), current_user:int  =  Depends(oauth2.get_current_user)):
    # deleting post
    # find the index in the array that has required ID

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # delete_posts = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized peform this action')
    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate,   db:Session = Depends(get_db), current_user:int  =  Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,id))
    # post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized peform this action')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()