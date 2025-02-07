from pydantic import BaseModel


class BaseCode(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "No message.",
            }
        }


# status code 200


class StatusCode201(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Create or update data.",
            }
        }


class StatusCode200(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "OK.",
            }
        }


# status code 400
class StatusCode400(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Bad Request message.",
            }
        }


class StatusCode401(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Unauthorized.",
            }
        }


class StatusCode403(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Forbidden message.",
            }
        }


class StatusCode409(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Conflict message.",
            }
        }


class StatusCode422(BaseCode):

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Field validation except message.",
            }
        }
