import streamlit as st
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def webScrapper(username, password, leaveType, visitPlace, stayAddress, rMob, sdt, edt, reason):
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)

    url = "https://ums.lpu.in/lpuums/"
    driver.get(url)

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtU"))
    )
    driver.execute_script("arguments[0].removeAttribute('onchange')", username_input)
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "TxtpwdAutoId_8767"))
    )
    password_input.send_keys(password)

    submit_button = driver.find_element("id", "iBtnLogins150203125")
    driver.execute_script("arguments[0].click();", submit_button)

    leave_url = "https://ums.lpu.in/lpuums/frmStudentHostelLeaveApplicationTermWise.aspx"
    driver.get(leave_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_ddlLeaveTerm"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//option[@value="Term-II"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_drpLeaveType"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//option[text()="{leaveType}"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_ddlVisitDay"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//option[@value="{visitPlace}"]'))
    ).click()

    sAdd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_txtPlaceToVisit"))
    )
    sAdd.send_keys(stayAddress)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_txtVisitingMobile"))
    ).send_keys(rMob)

    sdt_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ctl00_cphHeading_startdateRadDateTimePicker1_dateInput'))
    )
    driver.execute_script("arguments[0].removeAttribute('readonly')", sdt_element)
    sdt_element.send_keys(sdt)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_txtLeaveReason"))
    ).click()

    edt_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ctl00_cphHeading_enddateRadDateTimePicker2_dateInput'))
    )
    driver.execute_script("arguments[0].removeAttribute('readonly')", edt_element)
    edt_element.send_keys(edt)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_txtLeaveReason"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_txtLeaveReason"))
    ).send_keys(reason)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphHeading_btnSubmit"))
    ).click()

    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    st.write(f"Leave ID: {alert_text}")

# Function to validate mobile number
def validate_mobile_number(mobile):
    import re
    pattern = r"^\d{10}$"
    if re.match(pattern, mobile):
        return True
    else:
        return False

if __name__ == '__main__':
    options01 = ['Select', 'Night Leave', 'Day Leave', 'Day Leave(Extended Leave Timing)', 'Night Leave(Extended Leave Timing)', 'Vacation Leave']
    options02 = ['Select', 'Home', 'Local Guardian', 'Personal grooming', 'Medical checkup', "Due to Academic purposes", "Local Visit", "Out Station Visit", "Coaching", "Placement", "Other"]

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    leaveType = st.selectbox("Choose Leave Type", options01)
    visitPlace = st.selectbox("Visit Place", options02)
    stayAddress = st.text_area("Stay Address")
    reason = st.text_area("Reason of Leaving")
    mobile_number = st.text_input("Relative Mobile No.")

    rMob = ''
    if mobile_number:
        if validate_mobile_number(mobile_number):
            rMob = mobile_number
        else:
            st.error("Please enter a valid 10-digit mobile number.")
            mobile_number = None

    st.write("--( Kindly select date-times which could be applicable )--")
    sDate = st.date_input("Leave Start Date", value=None)
    sTime = st.time_input("Leave Start Time", value=None)
    eDate = st.date_input("Leave End Date", value=None)
    eTime = st.time_input("Leave End Time", value=None)

    if sDate is not None and sTime is not None and eDate is not None and eTime is not None:
        if sTime.hour > 12:
            sth = sTime.hour - 12
        else:
            sth = sTime.hour
        if sth < 1:
            sth = 12

        if eTime.hour > 12:
            eth = eTime.hour - 12
        else:
            eth = eTime.hour
        if eth < 1:
            eth = 12

        sdt = f'{sDate.month}/{sDate.day}/{sDate.year} {sth}:{sTime.minute}{" PM" if sTime.hour >= 12 else " AM"}'
        edt = f'{eDate.month}/{eDate.day}/{eDate.year} {eth}:{eTime.minute}{" PM" if eTime.hour >= 12 else " AM"}'

    if st.button("Submit"):
        if username == "":
            st.warning('Username field is required!')
        elif password == "":
            st.warning('Password field is required!')
        elif leaveType == 'Select':
            st.warning('Leave Type field is required!')
        elif visitPlace == 'Select':
            st.warning('Visit Place field is required!')
        elif stayAddress == "":
            st.warning('Stay Address field is required!')
        elif reason == "":
            st.warning('Reason of Leaving field is required!')
        elif mobile_number is None:
            st.warning('Relative Mobile No. field is required!')
        elif sDate is None or sTime is None or eDate is None or eTime is None:
            st.warning('Leave Start Date, Leave Start Time, Leave End Date, and Leave End Time fields are required!')
        else:
            try:
                webScrapper(username, password, leaveType, visitPlace, stayAddress, rMob, sdt, edt, reason)
            except Exception as e:
                st.write(e)
