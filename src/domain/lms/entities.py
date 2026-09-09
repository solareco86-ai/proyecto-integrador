"""Entidades de dominio del subdominio LMS (Cursos, Lecciones e Instructores)."""

from dataclasses import dataclass, field
from typing import Literal

from src.domain.common.value_objects import Price, Slug


@dataclass
class Instructor:
    id: str
    name: str
    role: str
    photo: str
    bio: str
    linkedin: str | None = None
    github: str | None = None
    twitter: str | None = None
    website: str | None = None


@dataclass
class Lesson:
    id: str
    slug: Slug
    title: str
    duration: str
    content_type: str = "markdown"
    video_url: str | None = None
    content: str | None = None
    type: Literal["lesson"] = "lesson"


@dataclass
class Question:
    id: str
    question: str
    type: str  # "single_choice" | "true_false"
    options: list[str]
    correct_option: int
    explanation: str | None = None


@dataclass
class Quiz:
    id: str
    slug: Slug
    title: str
    duration: str
    questions: list[Question] = field(default_factory=lambda: list[Question]())
    type: Literal["quiz"] = "quiz"


@dataclass
class CourseChapter:
    id: str
    title: str
    items: list[Lesson | Quiz] = field(default_factory=lambda: list[Lesson | Quiz]())
    description: str | None = None


@dataclass
class CourseSection:
    id: str
    title: str
    chapters: list[CourseChapter] = field(default_factory=lambda: list[CourseChapter]())
    description: str | None = None


@dataclass
class Course:
    id: str
    slug: Slug
    title: str
    description_short: str
    description_long: str
    duration: str
    level: str
    instructor: Instructor
    language: str = "Español"
    price: Price = Price(0.0)
    featured: bool = False
    academic_only: bool = False
    sections: list[CourseSection] = field(default_factory=lambda: list[CourseSection]())
