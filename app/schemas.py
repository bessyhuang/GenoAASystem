from bson.objectid import ObjectId
from pydantic import BaseModel, Field



### Select specific fields and display on FastAPI interface ###
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ClinicalModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    #No: str = Field(alias="No")
    SampleID: str = Field(alias="SampleID")
    Group: str = Field(alias="Group")
    Age: str = Field(alias="Age")
    LVMI: str = Field(alias="LVMI")
    microalbumin: str = Field(alias="microalbumin")
    Gender: str = Field(alias="Gender")
    ERT_drugs: str = Field(alias="ERT drugs")
    IVSD_before_ERT: str = Field(alias="IVSD before ERT")
    #Treatment_in_other_hospitals: str = Field(alias="Treatment in other hospitals")
    #date_of_birth: str = Field(alias="date of birth")
    #ERT_start_date: str = Field(alias="ERT start date")
    Heart_MRI_LGE: str = Field(alias="Heart MRI LGE (fibrosis)")
    Remark: str = Field(alias="Remark")
    #Medical_Record_Number: str = Field(alias="Medical record number")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
