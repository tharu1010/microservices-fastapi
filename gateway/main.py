from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any, Optional
from pydantic import BaseModel

# Models for request validation
class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    course: Optional[str] = None

class CourseCreate(BaseModel):
    name: str
    code: str

app = FastAPI(title="API Gateway", version="1.0.0")
API_KEY = "12345"

@app.middleware("http")

async def authenticate_request(request: Request, call_next):
    
    if request.url.path in ["/", "/docs", "/openapi.json"]:
        return await call_next(request)

   
    api_key = request.headers.get("X-API-Key")
    
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized: Invalid or Missing API Key"}
        )
    
    return await call_next(request)

SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:

    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{SERVICES[service]}{path}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}


@app.get("/gateway/students")
async def get_all_students():
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "GET")

@app.post("/gateway/students")
async def create_student(student: StudentCreate):
    return await forward_request("student", "/api/students", "POST", json=student.dict())

@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, student: StudentUpdate):
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=student.dict(exclude_unset=True))

@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")

# Course Service  Gateway Routes
@app.get("/gateway/courses")
async def get_all_courses():
    return await forward_request("course", "/api/courses", "GET")

@app.post("/gateway/courses")
async def create_course(course: CourseCreate):
    return await forward_request("course", "/api/courses", "POST", json=course.dict())

@app.put("/gateway/courses/{course_id}")
async def update_course(course_id: int, course: CourseCreate):
    return await forward_request("course", f"/api/courses/{course_id}", "PUT", json=course.dict())

@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int):
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")