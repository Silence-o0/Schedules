import datetime
import enum
from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, func, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from sqlalchemy.testing.schema import Table

from database import Base


class DayOfWeek(enum.Enum):
    MONDAY = "Понеділок"
    TUESDAY = "Вівторок"
    WEDNESDAY = "Середа"
    THURSDAY = "Четвер"
    FRIDAY = "П'ятниця"


class PairNum(enum.Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class TypeOfWeek(enum.Enum):
    BOTH = "Кожен тиждень"
    EVEN = "Парний"
    ODD = "Непарний"


class TypeOfLesson(enum.Enum):
    PRACTICE = "Практика"
    LECTURE = "Лекція"
    LAB = "Лабораторне заняття"
    SEMINAR = "Семінар"


class TeacherPosition(enum.Enum):
    ASSISTANT = "Асистент"
    LECTURER = "Доцент"
    PROFESSOR = "Професор"


GroupExam = Table(
    "GroupExam",
    Base.metadata,
    Column("exam_id", ForeignKey("Exam.id"), primary_key=True),
    Column("group_id", ForeignKey("Group.id"), primary_key=True)
)


ExamTeacher = Table(
    "ExamTeacher",
    Base.metadata,
    Column("exam_id", ForeignKey("Exam.id"), primary_key=True),
    Column("teacher_id", ForeignKey("Teacher.id"), primary_key=True)
)

GroupRecord = Table(
    "GroupRecord",
    Base.metadata,
    Column("group_id", ForeignKey("Group.id"), primary_key=True),
    Column("lesson_id", ForeignKey("RecordInSchedule.id"), primary_key=True)
)


class Group(Base):
    __tablename__ = "Group"

    id: Mapped[int] = mapped_column(primary_key=True)
    academic_term_id: Mapped[int] = mapped_column(ForeignKey("AcademicTerm.id"))
    field_of_study_id: Mapped[int] = mapped_column(ForeignKey("FieldOfStudy.id"))
    group_name: Mapped[str] = mapped_column(String(8), nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    field_of_study: Mapped["FieldOfStudy"] = relationship(back_populates="groups")
    academic_term: Mapped["AcademicTerm"] = relationship(back_populates="groups")
    exams: Mapped[List["Exam"]] = relationship(secondary=GroupExam, back_populates="groups")
    lessons: Mapped[List["RecordInSchedule"]] = relationship(secondary=GroupRecord, back_populates="groups")


class FieldOfStudy(Base):
    __tablename__ = "FieldOfStudy"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_title: Mapped[str] = mapped_column(String(2), nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    groups: Mapped[Group | None] = relationship(back_populates="field_of_study")


class AcademicTerm(Base):
    __tablename__ = "AcademicTerm"

    id: Mapped[int] = mapped_column(primary_key=True)
    academic_year_start: Mapped["AcademicYear"] = relationship(back_populates="term1")
    academic_year_finish: Mapped["AcademicYear"] = relationship(back_populates="term2")

    groups: Mapped[Group | None] = relationship(back_populates="academic_term")


class AcademicYear(Base):
    __tablename__ = "AcademicYear"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_year: Mapped[int] = mapped_column(nullable=False)
    term1_id: Mapped[int] = mapped_column(ForeignKey("AcademicTerm.id"))
    term2_id: Mapped[int] = mapped_column(ForeignKey("AcademicTerm.id"))

    term1: Mapped["AcademicTerm"] = relationship(back_populates="academic_year_start")
    term2: Mapped["AcademicTerm"] = relationship(back_populates="academic_year_finish")

    __table_args__ = (UniqueConstraint("term1_id"), UniqueConstraint("term2_id"), )


class Exam(Base):
    __tablename__ = "Exam"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("Subject.id"))
    date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    last_edited_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    groups: Mapped[List["Group"]] = relationship(secondary=GroupExam, back_populates="exams")
    teachers: Mapped[List["Teacher"]] = relationship(secondary=ExamTeacher, back_populates="exams")
    subject: Mapped["Subject"] = relationship(back_populates="exam")


class SubjectTeacher(Base):
    __tablename__ = "SubjectTeacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("Subject.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("Teacher.id"))
    type_of_lesson: Mapped[TypeOfLesson] = mapped_column(nullable=False)

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    subject: Mapped["Subject"] = relationship(back_populates="teachers")
    lessons: Mapped["RecordInSchedule"] = relationship(back_populates="subject_teacher")


class Teacher(Base):
    __tablename__ = "Teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    surname: Mapped[str] = mapped_column(String(40), nullable=False)
    first_name: Mapped[str] = mapped_column(String(40), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(40), nullable=True)
    email: Mapped[str] = mapped_column(String(40), nullable=True)
    position: Mapped[TeacherPosition] = mapped_column(nullable=True)
    birthdate: Mapped[datetime.datetime] = mapped_column(nullable=True)
    last_edited_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    exams: Mapped[List["Exam"]] = relationship(secondary=ExamTeacher, back_populates="teachers")
    subjects: Mapped[List["SubjectTeacher"]] = relationship(back_populates="teacher")


class Subject(Base):
    __tablename__ = "Subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_title: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(60), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    teachers: Mapped[List["SubjectTeacher"]] = relationship(back_populates="subject")
    exam: Mapped["Exam"] = relationship(back_populates="subject")


class RecordInSchedule(Base):
    __tablename__ = "RecordInSchedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_teacher_id: Mapped[int] = mapped_column(ForeignKey("SubjectTeacher.id"))
    pair_num: Mapped[PairNum] = mapped_column(nullable=False)
    day_of_week: Mapped[DayOfWeek] = mapped_column(nullable=False)
    type_of_week: Mapped[TypeOfWeek] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    teachers: Mapped[List["SubjectTeacher"]] = relationship(back_populates="subject")
    exam: Mapped["Exam"] = relationship(back_populates="subject")
    groups: Mapped[List["Group"]] = relationship(secondary=GroupRecord, back_populates="lessons")
    subject_teacher: Mapped["SubjectTeacher"] = relationship(back_populates="lessons")


class UserRole(Base):
    __tablename__ = "UserRole"
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("Role.id"), primary_key=True)
    assigned_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="roles")
    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):
    __tablename__ = "Role"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    users: Mapped[List["UserRole"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    last_edited_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    roles: Mapped[List["UserRole"]] = relationship(back_populates="user")




