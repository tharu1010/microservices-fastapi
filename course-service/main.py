from fastapi import FastAPI, HTTPException
from models import Course, CourseCreate
from typing import List

app = FastAPI(title="Course Microservice")

courses = [
    Course(id=1, name="Modern Topics in IT", code="IT4020")
]

# 1. all courses list
@app.get("/api/courses", response_model=List[Course])
def get_courses():
    return courses

# 2. add new course
@app.post("/api/courses", response_model=Course)
def create_course(course: CourseCreate):
    new_course = Course(id=len(courses)+1, **course.dict())
    courses.append(new_course)
    return new_course

# 3. course Update 
@app.put("/api/courses/{course_id}", response_model=Course)
def update_course(course_id: int, updated_course: CourseCreate):
    for i, course in enumerate(courses):
        if course.id == course_id:
            courses[i] = Course(id=course_id, **updated_course.dict())
            return courses[i]
    raise HTTPException(status_code=404, detail="Course not found")

# 4. course Delete 
@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):
    for i, course in enumerate(courses):
        if course.id == course_id:
            courses.pop(i)
            return {"message": "Course deleted successfully"}
    raise HTTPException(status_code=404, detail="Course not found")