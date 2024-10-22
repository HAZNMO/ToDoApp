from typing import Optional
from fastapi import Depends, Query
from to_do_app.dependences.auth.dependeces import decode_token
from to_do_app.domains.to_dos.schemas import TaskStatus
from to_do_app.Infrastructure.DB.mongo_db.mongo_construct import todo_collection

#mutat un service aici o chem
async def get_user_todos(
        user_info: dict = Depends(decode_token),
        task_status: Optional[TaskStatus] = Query(None, description="Task status to filter by (To Do, In Progress, Done)")):
    user_id = user_info.get("_id")
    query = {"user_id": user_id}

    if task_status is None:
        task_status = await todo_collection.find({"user_id": user_id}).to_list(1000)
        return task_status

    elif task_status:
        query["status"] = task_status

    todos = await todo_collection.find(query).to_list(1000)
    return todos