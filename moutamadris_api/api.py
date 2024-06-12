from requests import Session,exceptions
from bs4 import BeautifulSoup
from .moutamadris_classes import *
from .moutamadris_constants import *
from .moutamadris_enums import AdditionalInfos_Providers, AdditionalInfos_Types, Language, get_enum_by_value

def handle_request_exception(err):
        if isinstance(err, exceptions.ConnectionError):
            print("Connection error. Check your internet connection.")
        elif isinstance(err, exceptions.Timeout):
            print("Timeout error. The request took too long to complete.")
        elif isinstance(err, exceptions.HTTPError):
            print(f"HTTP error occurred: {err}")
        elif isinstance(err, exceptions.RequestException):
            print(f"An error occurred: {err}")
        else:
            print(f"An unknown error occurred: {err}")

def getRequestVerificationToken(session: Session,sourceUrl:str) -> str:
    response = session.get(sourceUrl,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    req_verification_input = soup.find('input', attrs={'name': '__RequestVerificationToken'})
    return req_verification_input.get("value")

def loginWithUsername_Password(username: str,password: str,session: Session)->str:
    #return idToken
    req_verification_token=getRequestVerificationToken(session,ACCOUNT_URL)
    form_data = {
      'UserName': username,
      'Password': password,
      '__RequestVerificationToken': req_verification_token
    }
    session.post(ACCOUNT_URL, data=form_data,headers=HEADERS)
    cookies = session.cookies.get_dict()
    return cookies["idToken"] if "idToken" in cookies else None

def isLogon(session:Session)->bool:
    return "idToken" in session.cookies.get_dict()

def loginWithIdToken(idToken: str,session: Session):
    session.cookies.set('idToken', idToken)

def getSoupFromUrl(url: str,session: Session)-> BeautifulSoup:
    response = session.get(url,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def postData(url: str,form_data: str,session:Session)-> BeautifulSoup:
    response = session.post(url,data=form_data,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def getAccountInfos(session:Session)->AccountInfos:
    soup:BeautifulSoup=getSoupFromUrl(ACCOUNT_INFO_URL,session=session)
    main_element=soup.find('dd', attrs={'id': 'codeEleve'})
    if not main_element:
        return None
    children=main_element.parent.parent.parent.findChildren("dd" , recursive=True)
    studentCode: str=main_element.text
    firstName: str=children[1].text
    lastName: str=children[2].text
    placeOfBirth: str=children[6].text
    gender: str=children[7].text
    school: str=children[8].text
    academy:str=children[9].text
    provincialDirectorate:str=children[10].text
    parentFirstName: str=children[3].text
    parentLastName: str=children[4].text
    parentPhoneNumber: str=children[5].text
    personal_infos= PersonalInfos(studentCode, firstName,lastName,placeOfBirth,gender,school,academy,provincialDirectorate,parentFirstName,parentLastName,parentPhoneNumber)
    provider=soup.find('select', attrs={'id': 'Operateur'}).select_one('option:checked').get("value")
    phoneNumber=soup.find('input', attrs={'id': 'Tel'}).get("value")
    alltypes=soup.find_all('input', attrs={'id': 'Type','type':'radio','checked':'checked'})
    type="Père"
    if len(alltypes)>1:
        type=alltypes[1].get("value")
    else:
        type=alltypes[0].get("value")
    additional_infos=AdditionalInfos(provider=get_enum_by_value(provider,AdditionalInfos_Providers),phoneNumber=phoneNumber,type=get_enum_by_value(type,AdditionalInfos_Types))
    recoveryEmail=soup.find('input', attrs={'id': 'EmailPerso'}).get("value")
    return AccountInfos(personalInfos=personal_infos,additionalInfos=additional_infos,recoveryEmail=recoveryEmail)

def updateAdditionalInfos(session:Session,provider:AdditionalInfos_Providers,type:AdditionalInfos_Types,phoneNumber:str)->bool:
    form_data = {
      'UpdateTel': 'False',
      'Operateur': provider.value,
      'Tel': phoneNumber,
      'Type': type.value
    }
    response = session.post(ADDITIONAL_INFOS_UPDATE_URL,data=form_data,headers=HEADERS)
    return bool(response.content)

def updateRecoveryEmail(session:Session,email:str)->bool:
    form_data = {
      'EmailPerso': email,
      'UpdateEmail': 'False',
    }
    response = session.post(ADDITIONAL_INFOS_UPDATE_URL,data=form_data,headers=HEADERS)
    return bool(response.content)

def resetMFA(session:Session)->bool:
    response = session.post(RESET_MFA_URL,headers=HEADERS)
    return bool(response.content)

def getEducationalPeriod(session)->EducationalPeriods:
    soup:BeautifulSoup=getSoupFromUrl(EDUCATIONAL_PERIOD_URL,session=session)
    years:list[SchoolYear]=[]
    years_options=soup.find("select",attrs={'id':'SelectedAnnee'}).find_all('option')
    for option in years_options:
        years.append(SchoolYear(option.get("value"),option.text))
    sessions:list[SchoolSession]=[]
    sessions_options=soup.find("select",attrs={'id':'SelectedSession'}).find_all('option')
    for option in sessions_options:
         sessions.append(SchoolSession(option.text,option.get("value")))
    return EducationalPeriods(years,sessions)

def extractTableData(soup,table_id):
    table_data = {}
    table = soup.select_one(f'{table_id} table')
    headers = [th.get_text(strip=True) for th in table.find_all('th')]    
    current_matiere = None
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if cells:
            if 'rowspan' in cells[0].attrs:
                current_matiere = cells[0].get_text(strip=True)
                data = {headers[i]: cells[i].get_text(strip=True) for i in range(len(cells))}
                if current_matiere not in table_data:
                    table_data[current_matiere] = []
                table_data[current_matiere].append(data)
            else:
                data = {headers[i+1]: cells[i].get_text(strip=True) for i in range(len(cells))}
                table_data[current_matiere].append(data)    
    return table_data

def getAllMarks(session:Session,studyYearID:str,sessionID)->Marks:
    form_data={
        'Annee':studyYearID,
        'IdSession':sessionID
    }
    soup=postData(MARKS_URL,form_data,session)
    table_cc = extractTableData(soup,'#tab_cc')
    table_exam = extractTableData(soup,'#tab_notes_exam')
    divs_with_border_top = soup.find_all('div', style=lambda value: value and 'border-top: 1px solid #f3f3f3;' in value)
    results = {}
    schoolDetails = {}
    for div in divs_with_border_top:
        label = div.find('label')
        if label:
            key = label.get_text(strip=True)
            span = div.find('span')
            if span:
                value = span.get_text(strip=True)
                results[key] = value

    dt_elements = soup.find_all('dt')
    for dt in dt_elements:
        key = dt.get_text(strip=True)
        dd = dt.find_next_sibling('dd')
        if dd:
            value = dd.get_text(strip=True)
            schoolDetails[key] = value  
    return Marks(continuousAssessmentMarks=table_cc,averageMarks=table_exam,resultMark=results,schoolDetails=schoolDetails)

def changeLanguage(session:Session,language:Language):
    session.post(f'{SWITCH_LANGUAGE_URL}{language.value}',headers=HEADERS)

def getMyAcademicJourney(session:Session)->list[ResultMark]:
    academicJourney:list[ResultMark]=[]
    soup=getSoupFromUrl(ACADEMIC_JOURNEY_URL,session)
    alltrs=soup.find("tbody").find_all('tr')
    for tr in alltrs:
        schoolYear:str=tr.find('td',attrs={'data-name':'AnneeScolaire'}).get_text(strip=True)
        school:str=tr.find('td',attrs={'data-name':'Etablissement'}).get_text(strip=True)
        gradeLevel:str=tr.find('td',attrs={'data-name':'Niveau'}).get_text(strip=True)
        averageMark:str=tr.find('td',attrs={'data-name':'Moyenne'}).get_text(strip=True)
        finalResult:str=tr.find('td',attrs={'data-name':'resultat'}).get_text(strip=True)
        academicJourney.append(ResultMark(schoolYear,school,gradeLevel,averageMark,finalResult))
    return academicJourney

def getIDToken(session:Session)->str:
    if isLogon(session=session):
        return session.cookies.get_dict()["idToken"]
    else:
        return None
    
def changePassword(session:Session,oldPassword:str,newPassword:str):
    form_data={
        'Password':oldPassword,
        'NewPassword':newPassword,
        'NewPasswordConfirm':newPassword,
        '__RequestVerificationToken':getRequestVerificationToken(session,CHANGE_PASSWORD_URL)
    }
    session.post(CHANGE_PASSWORD_URL,form_data,session,headers=HEADERS)

class IncorrectCredentialsError(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)
