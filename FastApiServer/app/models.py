from pydantic import BaseModel


class ExponeaRequestModel(BaseModel):
    timeout: int

    class Config:
        schema_extra = {
            "example": {"timeout": 300},
        }


class ExponeaSuccessReponse(BaseModel):
    timeout: int

    class Config:
        schema_extra = {
            "example": {"timeout": 300},
        }


class ExponeaErrorResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {"message": "ExponeaError"},
        }
