from dataclasses import dataclass

from .moutamadris_enums import AdditionalInfos_Providers, AdditionalInfos_Types

@dataclass
class PersonalInfos:
    studentCode: str
    firstName: str
    lastName: str
    placeOfBirth: str
    gender: str
    school: str
    academy:str
    provincialDirectorate:str
    parentFirstName: str
    parentLastName: str
    parentPhoneNumber: str
    def __init__(self, studentCode, firstName,lastName,placeOfBirth,gender,school,academy,provincialDirectorate,parentFirstName,parentLastName,parentPhoneNumber):
        self.studentCode = studentCode
        self.firstName = firstName
        self.lastName = lastName
        self.placeOfBirth = placeOfBirth
        self.gender = gender
        self.school = school
        self.academy = academy
        self.provincialDirectorate = provincialDirectorate
        self.parentFirstName = parentFirstName
        self.parentLastName = parentLastName
        self.parentPhoneNumber = parentPhoneNumber

@dataclass
class AdditionalInfos:
    provider: AdditionalInfos_Providers
    phoneNumber: str
    type:AdditionalInfos_Types
    def __init__(self,provider:AdditionalInfos_Providers,phoneNumber:str,type:AdditionalInfos_Types):
        self.provider=provider
        self.phoneNumber=phoneNumber
        self.type=type


@dataclass
class SchoolSession:
    schoolSession:str
    sessionID:str
    def __init__(self,schoolSession,sessionID):
        self.schoolSession=schoolSession
        self.sessionID=sessionID

@dataclass
class SchoolYear:
    schoolYear:str
    schoolyearID:str
    def __init__(self,schoolyearID,schoolYear):
        self.schoolYear=schoolYear
        self.schoolyearID=schoolyearID

@dataclass
class EducationalPeriods:
    schoolYears:list[SchoolYear]
    sessions:list[SchoolSession]
    def __init__(self,schoolYears,sessions):
        self.schoolYears=schoolYears
        self.sessions=sessions

@dataclass
class AccountInfos:
    personalInfos: PersonalInfos
    additionalInfos:AdditionalInfos
    recoveryEmail:str
    def __init__(self,personalInfos:PersonalInfos,additionalInfos:AdditionalInfos,recoveryEmail:str):
        self.personalInfos=personalInfos
        self.additionalInfos=additionalInfos
        self.recoveryEmail=recoveryEmail


@dataclass
class Marks:
    continuousAssessmentMarks:dict
    averageMarks:dict
    resultMark:dict[str,str]
    schoolDetails:dict[str,str]
    def __init__(self,continuousAssessmentMarks,averageMarks,resultMark,schoolDetails):
        self.continuousAssessmentMarks=continuousAssessmentMarks
        self.averageMarks=averageMarks
        self.resultMark=resultMark
        self.schoolDetails=schoolDetails

@dataclass
class ResultMark():
    schoolYear:str
    school:str
    gradeLevel:str
    averageMark:str
    finalResult:str
    def __init__(self,schoolYear,school,gradeLevel,averageMark,finalResult):
        self.schoolYear=schoolYear
        self.school=school
        self.gradeLevel=gradeLevel
        self.averageMark=averageMark
        self.finalResult=finalResult