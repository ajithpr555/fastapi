from fastapi import  status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. schemas import Vote,UserOut
from .. import models,oauth2
from ..database import get_db

router=APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def votes(vote: Vote,db: Session = Depends(get_db), current_user: UserOut = Depends(oauth2.get_current_user)):
    
    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f'post with {vote.post_id} not found')
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    print(vote_query)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {current_user.id} already voted on {vote.post_id}')
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"sucessfully added vote"}
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message":"sucessfully deleted vote"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'user {current_user.id} has not voted on {vote.post_id}')
            
            
        
    
    
