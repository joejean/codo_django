from selenium import webdriver

browser = webdriver.Firefox()
browser.implicitly_wait(4)

browser.get("http://localhost:8000/")
browser.find_element_by_id("start_campaign").click()

email = browser.find_element_by_id("id_login")
email.send_keys("julia@test.com")
password = browser.find_element_by_id("id_password")
password.send_keys("police12345")
password.submit()
title = browser.find_element_by_id("id_campaign_info-title")
title.send_keys("Better Back Campaign")
blurb = browser.find_element_by_id("id_campaign_info-blurb")
blurb.send_keys("Fix your Posture")
category = browser.find_element_by_xpath("//select[@id='id_campaign_info-category']/option[@value='art']").click()
description = browser.find_element_by_id("id_campaign_info-title")
description.send_keys("""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""")

picture = browser.find_element_by_id("id_campaign_info-picture")
picture.send_keys(r"/home/joe/Pictures/happy.jpg")

video_url = browser.find_element_by_id("id_campaign_info-video_url")
video_url.send_keys("https://www.youtube.com/watch?v=RgKAFK5djSk")

goal_amount = browser.find_element_by_id("id_campaign_info-goal_amount")
goal_amount.send_keys("200")

end_date = browser.find_element_by_id("id_campaign_info-end_date")
end_date.send_keys("2016-04-30")


conditionals_enabled = browser.find_element_by_id("id_campaign_info-conditionals_enabled")
conditionals_enabled.submit()

country =  browser.find_element_by_xpath("//select[@id='id_organizer_info-country']/option[@value='AE']").click()

phone_number = browser.find_element_by_id("id_organizer_info-phone_number")
phone_number.send_keys("+971501067468")

short_bio = browser.find_element_by_id("id_organizer_info-short_bio")
short_bio.send_keys("""Duis aute irure dolor in reprehenderit in voluptate velit essecillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""")

profile_picture = browser.find_element_by_id("id_organizer_info-profile_picture")
profile_picture.send_keys(r"/home/joe/Pictures/citadelle.jpg")


facebook = browser.find_element_by_id("id_organizer_info-facebook_url")
facebook.send_keys("https://www.joejean.net")

twitter = browser.find_element_by_id("id_organizer_info-twitter_url")
twitter.send_keys("https://www.joejean.net")

website_url = browser.find_element_by_id("id_organizer_info-website_url")
website_url.send_keys("https://www.joejean.net")

dob = browser.find_element_by_id("id_organizer_info-dob")
dob.submit()

login_wepay = browser.find_element_by_xpath("//span[@id='authorize-login']/a[1]").click()

email = browser.find_element_by_name("email")
email.send_keys("mrjoe.jean@gmail.com")
password = browser.find_element_by_name("password")
password.send_keys("police12345")
password.submit()
#browser.quit()



