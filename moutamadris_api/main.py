from .api import *
from .moutamadris_classes import AccountInfos, EducationalPeriods, Marks, ResultMark
from .moutamadris_enums import Language

class moutamadris:
    def __init__(self, email:str=None, password:str=None, idToken:str=None):
        """
        Moutamadris API made by Abdellah El idrissi
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        \nMy github account: https://github.com/AbdellahDeveloper\n
---------------------------
        \nInitialize the moutamadris API with email and password or an ID token
        \nArgs:
        \n- email: Your Email (ex: XXXXXXXXX@taalim.ma)
        \n- password: Your Moutamadris Account Password
        \nor :
        \n- idToken: Moutamadris ID token for authentication
        """
        self.session = Session()
        if email and password:
            loginWithUsername_Password(email, password, self.session)
        elif idToken:
            loginWithIdToken(idToken, session=self.session)
        if not isLogon(self.session):
            raise IncorrectCredentialsError('The provided credentials are incorrect')

    def GetIdToken(self) -> str:
        """
        Retrieve the ID token for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - str: The ID token for the logged-in user.
        """
        return getIDToken(self.session)

    def GetAccountInfos(self) -> AccountInfos:
        """
        Retrieve account informations for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - AccountInfos: Informations about the logged-in user's account.
        """
        try:
            return getAccountInfos(session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def GetEducationalPeriod(self) -> EducationalPeriods:
        """
        Retrieve informations about the current educational period.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - EducationalPeriod: all existing sessionIDs and studyYearsIDs
        """
        try:
            return getEducationalPeriod(session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def GetAllMarks(self, studyYearID: str, sessionID: str) -> Marks:
        """
        Retrieve all marks for a given study year and session.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Args:
        - studyYearID: Identifier for the study year. (from: GetEducationalPeriod)
        - sessionID: Identifier for the session. (from: GetEducationalPeriod)

        Returns:
        - Marks: All marks for the specified study year and session.
        """
        try:
            return getAllMarks(studyYearID=studyYearID, sessionID=sessionID, session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def GetAcademicJourney(self) -> list[ResultMark]:
        """
        Retrieve the academic journey of the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - list[ResultMark]: The academic journey of the logged-in user.
        """
        try:
            return getMyAcademicJourney(session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def UpdateAdditionalInfos(self, provider: AdditionalInfos_Providers, type: AdditionalInfos_Types,
                              phoneNumber: str) -> bool:
        """
        Update additional information for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Args:
        - provider: telecommunications provider
        - type: Type of phone number owner.
        - phoneNumber: Phone number associated with the additional information.

        Returns:
        - bool: True if the information is successfully updated, False otherwise.
        """
        try:
            return updateAdditionalInfos(provider=provider, type=type, phoneNumber=phoneNumber,
                                             session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def UpdateRecoveryEmail(self, email: str) -> bool:
        """
        Update the recovery email address for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Args:
        - email: New recovery email address.

        Returns:
        - bool: True if the email is successfully updated, False otherwise.
        """
        try:
            return updateRecoveryEmail(email=email, session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def ResetMFA(self) -> bool:
        """
        Reset the Multi-Factor Authentication (MFA) for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - bool: True if MFA is successfully reset, False otherwise.
        """
        try:
            return resetMFA(session=self.session)
        except Exception as err:
            handle_request_exception(err=err)

    def ChangePassword(self, old_password: str, new_password: str) -> None:
        """
        Change the password for the logged-in user.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Args:
        - old_password: Current password.
        - new_password: New password.

        Raises:
        - Exception: If an error occurs while changing the password.
        """
        changePassword(oldPassword=old_password, newPassword=new_password, session=self.session)

    def ChangeMoutamadrisLanguage(self, language: Language) -> None:
        """
        Change the language preference for the Moutamadris 
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Args:
        - language: Desired language for the Moutamadris 

        Raises:
        - Exception: If an error occurs while changing the language.
        """
        return changeLanguage(language=language, session=self.session)

    def isLoggedin(self) -> bool:
        """
        Check if the user is currently logged in.
        ~~~~~~~~~~~~~~~~~~~~~
        ---------------------------
        
        Returns:
        - bool: True if the user is logged in, False otherwise.
        """
        return isLogon(session=self.session)