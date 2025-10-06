from typing import List
from ..database import get_db
from fastapi import  status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. schemas import PostBase,PostCreate,TokenData,PostOut
from .. import models,oauth2
from typing import Optional
from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=['Posts'])


#response_model=List[PostCreate]
@router.get("/",response_model=List[PostOut])
def get_posts(db : Session = Depends(get_db), limit:int = 10, skip:int =0, search: Optional[str]=""):
    
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
   
    return posts
    # cursor.execute('''select * from posts''')
    # posts=cursor.fetchall()
    # return {"data":posts}
    
@router.get("/{id}",response_model=PostOut)
def get_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute('''select * from posts where id = %s''',(str(id)))
    # post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == id, isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    return post



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=PostCreate)
def create_posts(post:PostBase,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session = Depends(get_db),current_user: int  = Depends(oauth2.get_current_user)):
    # 
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not present")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authroized to perform requested operation")

    post.delete(synchronize_session= False)
    db.commit()

    return post
@router.put("/{id}",response_model=PostBase)
def update_posts(post:PostBase,id:int,db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    
    
    # cursor.execute("""UPDATE posts SET title= %s, content = %s,published = %s where id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # post=cursor.fetchone()
    # conn.commit()
    
    update_post_query= db.query(models.Post).filter(models.Post.id == id)
    
    update_post= update_post_query.first()
    
    if not update_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no post with id {id} found")
    
    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authroized to perform requested operation")

    update_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return update_post.first()