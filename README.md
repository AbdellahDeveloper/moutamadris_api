# Unofficial Moutamadris API for Python 💻

![Static Badge](https://img.shields.io/badge/Awesome%20API-8A2BE2?logo=windows&logoColor=white)

## Installation ⚙️

To install it, use:

```bash
pip install moutamadris_api
```

## Usage ✍

### Import Moutamadris Package

```python
from moutamadris_api import moutamadris,moutamadris_enums
```
## Create Instance Of Moutamadris
Replace **email** and **password** with yours:

```python
moutamadris_instance = moutamadris('your_email@taalim.ma', 'your_password')
```
## Available Functions

### Account Management
```python
moutamadris_instance.GetAccountInfos() # Get all account info such as firstname, lastname...
moutamadris_instance.GetEducationalPeriod() # Get current educational period details
moutamadris_instance.GetIdToken() # Retrieve the ID token for the logged-in user
moutamadris_instance.UpdateAdditionalInfos(provider, type, phoneNumber) # Update additional information
moutamadris_instance.UpdateRecoveryEmail('new_email@example.com') # Update recovery email
moutamadris_instance.ResetMFA() # Reset Multi-Factor Authentication
moutamadris_instance.ChangePassword('old_password', 'new_password') # Change password
moutamadris_instance.ChangeMoutamadrisLanguage(Language.FRENCH) # Change API language preference
moutamadris_instance.isLoggedin() # Check if user is logged in
```

### Marks
```python
moutamadris_instance.GetAllMarks('studyYearID', 'sessionID') # Retrieve all marks for a given study year and session
moutamadris_instance.GetAcademicJourney() # Retrieve the academic journey of the logged-in user
```

## 🛠 Built With
![Static Badge](https://img.shields.io/badge/Python%203.10-6b32fa?logo=python&logoColor=white)

## Hi, I'm Abdellah Elidrissi! 👋

Passionate developer and student with a diverse skill set that spans across various domains. From Web Development utilizing technologies like Asp.net Core MVC, Node.js, HTML, CSS, JavaScript, and React, to Android Development with expertise in Java and Flutter, I've ventured into Desktop Development using WinForms in C# and even dived into the world of Games Development, specializing in Unreal Engine. Additionally, I have a knack for 3D Design, leveraging tools like Blender to bring creative ideas to life.

I embarked on this journey in the world of programming at the age of 13, and my trajectory has been a fascinating evolution, starting from desktop applications to conquering the realms of Android, Games, and finally Web Development. Currently, I'm studying at ENSA MARRAKECH.

With a genuine love for programming, I find joy in turning concepts into functional and aesthetically pleasing applications. I'm excited to see what challenges and innovations lie ahead in this ever-evolving field.
