from datetime import datetime, time, timedelta
from typing import List, Optional

from fastapi import Body, FastAPI

from pydantic import BaseModel, Field, HttpUrl

from uuid import UUID

class Video(BaseModel):
    url: HttpUrl
    name: str
    description: Optional[str] = Field(
        None, title="The description of the course", max_length=300
    )


class Course(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the course", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None
    videos: Optional[List[Video]] = None

class CourseSet(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    courses: List[Course]

fast_courses = FastAPI()

fake_courses_db = [{"course_name": "Foo"}, {"course_name": "Bar"}, {"course_name": "Baz"}]

@fast_courses.get("/courses/")
async def read_course(skip: int = 0, limit: int = 10):
    return fake_courses_db[skip : skip + limit]

@fast_courses.get("/courses/{course_id}")
async def read_user_course(
     course_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    course = {"course_id": course_id, "needy": needy, "skip": skip, "limit": limit}
    return course

@fast_courses.post("/courses/")
async def create_course(course: Course):
    return course

@fast_courses.put("/courses/{course_id}")
async def read_courses(
    course_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "course_id": course_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

@fast_courses.post("/course-sets/")
async def create_course_set(course_set: CourseSet):
    return course_set

@fast_courses.post("/videos/multiple/")
async def create_multiple_videos(videos: List[Video]):
    return videos