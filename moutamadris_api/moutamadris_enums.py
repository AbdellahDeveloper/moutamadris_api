from enum import Enum
 
class AdditionalInfos_Types(Enum):
    MOTHER = "Mère"
    FATHER = "Père"
    PERSONAL = "Eleve"
    TUTOR = "Tuteur"
    NONE=''

class AdditionalInfos_Providers(Enum):
    IAM = "Iam"
    ORANGE = "Orange"
    INWI = "Inwi"
    OTHER = "Autre"
    NONE=''

class Language(Enum):
    ARABIC = "ar"
    FRENCH = "fr"

def get_enum_by_value(value,enum):
    for item in enum:
        if item.value == value:
            return item
    return None