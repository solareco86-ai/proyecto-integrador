"""DTOs de Pydantic para el subdominio de cursos (LMS), lecciones e instructores."""

from typing import Literal

from pydantic import BaseModel, Field


class InstructorSocialLinksModel(BaseModel):
    linkedin: str | None = None
    github: str | None = None
    twitter: str | None = None
    website: str | None = None


class InstructorModel(BaseModel):
    id: str
    name: str
    role: str
    photo: str
    photo_width: int | None = None
    photo_height: int | None = None
    bio: str
    social_links: InstructorSocialLinksModel | None = None


class InstructoresContainerModel(BaseModel):
    instructores: list[InstructorModel]


class LessonModel(BaseModel):
    type: Literal["lesson"] = "lesson"
    id: str
    slug: str
    title: str = Field(..., min_length=1)
    duration: str
    content_type: str = "markdown"
    video_url: str | None = None
    content: str | None = None
    content_file: str | None = None


class QuestionModel(BaseModel):
    id: str
    question: str
    type: str  # "single_choice" | "true_false"
    options: list[str]
    correct_option: int  # Índice de la opción correcta (0-indexed)
    explanation: str | None = None


class QuizModel(BaseModel):
    type: Literal["quiz"] = "quiz"
    id: str
    slug: str
    title: str = Field(..., min_length=1)
    duration: str
    questions: list[QuestionModel]


class CourseChapterModel(BaseModel):
    id: str
    title: str
    description: str | None = None
    items: list[LessonModel | QuizModel]


class CourseSectionModel(BaseModel):
    id: str
    title: str
    description: str | None = None
    chapters: list[CourseChapterModel]


class CourseModel(BaseModel):
    id: str
    slug: str
    title: str = Field(..., min_length=1)
    description_short: str = Field(..., min_length=1)
    description_long: str = Field(..., min_length=1)
    duration: str
    level: str
    language: str = "Español"
    price: float = 0.0
    og_image: str | None = None
    og_image_width: int | None = None
    og_image_height: int | None = None
    featured: bool = False
    academic_only: bool = False
    instructor: InstructorModel
    sections: list[CourseSectionModel]


class CursosContainerModel(BaseModel):
    cursos: list[CourseModel]
