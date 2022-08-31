# -*- coding: utf-8 -*-
"""
Updated on Aug 30 21:40:10 2022

@author: MrMenezes
"""

#system libraries
import os
import random
import time
import urllib

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#recaptcha libraries
import speech_recognition as sr

def recognize():
    import subprocess
    subprocess.Popen(["ffmpeg/bin/ffmpeg.exe", "-y", "-i", "sample.mp3", "sample.wav"]).wait()
    sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
    r= sr.Recognizer()

    with sample_audio as source:
        audio = r.record(source)

    #translate audio to text with google voice recognition
    key=r.recognize_google(audio)    

    return key

def delay ():
    time.sleep(random.randint(2,3))

def download(driver, actions):

    #switch to recaptcha frame
    frame=driver.find_element(By.XPATH, "//iframe")
    driver.switch_to.frame(frame)
    delay()

    #click on checkbox to activate recaptcha
    check = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
    actions.click(check)

    #switch to recaptcha audio control frame
    driver.switch_to.default_content()
    audio_frame = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/iframe")
    driver.switch_to.frame(audio_frame)
    delay()

    #click on audio challenge
    audio_button = driver.find_element(By.ID, "recaptcha-audio-button").click()
    actions.click(audio_button)

    #switch to recaptcha audio challenge frame
    driver.switch_to.default_content()
    frames=driver.find_elements(By.XPATH, "//iframe")
    driver.switch_to.frame(frames[-1])
    delay()

    #click on the play button
    driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/button").click()
    #get the mp3 audio file
    src = driver.find_element(By.ID,"audio-source").get_attribute("src")
    print("[INFO] Audio src: %s"%src)
    #download the mp3 audio file from the source
    urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")

def bypass(driver, actions, key):
    #key in results and submit
    driver.find_element(By.ID, "audio-response").send_keys(key.lower())
    driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()
    delay()
    submit = driver.find_element(By.ID, "recaptcha-demo-submit")
    actions.click(submit)
    delay()

try:
    #create chrome driver
    path = os.getcwd()+"\\webdriver\\chromedriver.exe"
    driver = webdriver.Chrome(path) 
    delay()
    #go to website
    driver.get("https://www.google.com/recaptcha/api2/demo")

except Exception as err: 
    print(err)
    print("[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

actions = ActionChains(driver)

download(driver, actions)
key = recognize()
print("[INFO] Recaptcha Passcode: %s"%key)
bypass(driver, actions,key)

