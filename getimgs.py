from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import datetime

random.seed()
url = 'https://www.nicview.net/default'
savedir = '/run/media/darin/easystore/SKC/'
nicviewuser = "your_nicview_user"
nicviewpw = "your_nicview_password"


def get_screenshots():
    try:
        #initialize selenium webdriver and get the url
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        driver.get(url)

        #find the login button and click on it
        login = driver.find_element_by_name("signInButton")
        login.click()

        #sleep for a random interval so things can load
        #should really wait for elements, but this works
        time.sleep(random.randint(2, 7))

        #find elements we want
        theuser = driver.find_element_by_name("username")
        thepw = driver.find_element_by_name("password")
        loginbutton = driver.find_element_by_name("submit")

        #sleep again
        time.sleep(random.randint(1, 6))

        #input credentials and log in
        theuser.send_keys(nicviewuser)
        thepw.send_keys(nicviewpw)
        loginbutton.click()

        #sleep again
        time.sleep(random.randint(2, 5))

        #escape to get to liveViewer and find liveViewer
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(random.randint(2, 5))
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        theimg = driver.find_element_by_id("liveViewer")

        imglist = []
        lastsrc = ''
        lastsrccnt = 0

        #run a while loop checking for what we want
        #recycle eventually if we don't find it
        while lastsrccnt < 1000:
            #try to find it
            try:
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                theimg = driver.find_element_by_id("liveViewer")
                thesrc = theimg.get_property('src')
            #on exception, sleep, try to find it again
            except Exception as e:
                print(e)
                time.sleep(10)
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                theimg = driver.find_element_by_id("liveViewer")
                thesrc = theimg.get_property('src')
            #if we found it, start looking for images
            #save those images if we don't already have them
            if thesrc != lastsrc and thesrc not in imglist:
                imglist.append(thesrc)
                lastsrccnt = 0
                filename = savedir + thesrc.split('.')[-1] + '.png'
                with open(filename, 'wb') as file:
                    file.write(theimg.screenshot_as_png)
                    theimg.click()
            #if we did not find elements
            #and did not throw exception
            #incremenet lastsrccnt
            else:
                lastsrccnt += 1
            lastsrc = thesrc
        #nurse is caring...
        #quit after 1000 loops
        driver.quit()

    except Exception as e:
        print(e)
        driver.quit()


#run until killed manually
while True:
    get_screenshots()
