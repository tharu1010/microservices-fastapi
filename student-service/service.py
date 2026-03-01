from data_service import StudentMockDataService
from models import StudentCreate, StudentUpdate
from typing import List, Optional

class StudentService:
    def __init__(self):
        self.data_service = StudentMockDataService()
    
    def get_all(self):
        return self.data_service.get_all_students()
    
    def get_by_id(self, student_id: int):
        return self.data_service.get_student_by_id(student_id)
    
    def create(self, student: StudentCreate):
        return self.data_service.add_student(student)
    
    def update(self, student_id: int, student: StudentUpdate):
        return self.data_service.update_student(student_id, student)
    
    def delete(self, student_id: int):
        return self.data_service.delete_student(student_id)
