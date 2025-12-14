"""Data models for notes."""

from pydantic import BaseModel, Field, field_validator

from src.managers.encryption.cipher import Cipher

cipher = Cipher()


class NoteData(BaseModel):
    """Data model for a note's metadata."""

    id: int = Field(...)
    title: str = Field(...)
    date: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")

    @field_validator("title", mode="after")
    @classmethod
    def title_decode(cls, v: str) -> str:
        """Decode the title."""
        return cipher.decode(v)


class NewNoteData(BaseModel):
    """Data model for creating a new note."""

    title: str = Field(...)
    content: str = Field(...)
    date: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")

    @field_validator("title", mode="after")
    @classmethod
    def title_encode(cls, v: str) -> str:
        """Encode the title."""
        return cipher.encode(v)

    @field_validator("content", mode="after")
    @classmethod
    def content_encode(cls, v: str) -> str:
        """Encode the content."""
        return cipher.encode(v)


class ModifyNoteData(BaseModel):
    """Data model for modifying an existing note."""

    id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    date: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")

    @field_validator("title", mode="after")
    @classmethod
    def title_encode(cls, v: str) -> str:
        """Encode the title."""
        return cipher.encode(v)

    @field_validator("content", mode="after")
    @classmethod
    def content_encode(cls, v: str) -> str:
        """Encode the content."""
        return cipher.encode(v)


class NoteContentData(BaseModel):
    """Data model for a note's full content."""

    content: str = Field(...)

    @field_validator("content", mode="after")
    @classmethod
    def content_decode(cls, v: str) -> str:
        """Decode the content."""
        return cipher.decode(v)
