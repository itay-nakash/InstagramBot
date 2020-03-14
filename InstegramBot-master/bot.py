from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class InstagramBot:
    """"
    Initializes an instance of the InstagramBot class.

    Call the login method to authenticate a user with IG
    Args:
        username:str: The Instagram username for a user
        password:str The Instagram password for a user

    Attributes:
        driver:Selenium.webdriver.Chrome: The Chromdriver that is used to automate browser action
        wait:
    """

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = 'https://www.instagram.com'
        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        log_in_button = self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]")
        ActionChains(self.driver).move_to_element(log_in_button).click().perform()
        self.wait.until(ec.invisibility_of_element((By.XPATH, '//*[contains(text(), "Sign up")]')))

    # should understand if it navigating to an hashtag or to a user
    def nav_page(self, url_add_text):
        self.driver.get('{}/{}/'.format(self.base_url, url_add_text))

    def scroll_down(self):
        body_elem = self.driver.find_element_by_tag_name('body')

        # move up and down 3 times to load new images
        for _ in range(3):
            body_elem.send_keys(Keys.END)
            time.sleep(1)  # TODO change the sleep to a better function
            body_elem.send_keys(Keys.HOME)
            time.sleep(1)

    """
    function that activate the navigation function to the user page and follow/Unfollow him
    follow_order - the text according to the act you want to do. Follow for following a user and Following for unfollow
    """

    def follow_action(self, user, follow_order):
        self.nav_page(user)
        follow_text_element = self.driver.find_element_by_xpath('//button[contains(text(),"' + follow_order + '")]')
        follow_text_element.click()
        if follow_order == "Following":
            follow_text_element = self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
            follow_text_element.click()

    def like_picture(self, hashtag):
        pics = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, tagged="' '//a[contains(@href, '
                                                           '"tagged=yariv")]')))
        links = [pic.get_attribute("href") for pic in pics]
        for link in links:
            self.driver.get(link)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "coreSpriteHeartOpen")]'))).click()

    def testLike(self):
        link_to_heart = self.driver.find_element_by_xpath('/htmlhow to /body')
        link_to_heart.click()

    """""
    function that get to the comment button, click it and insert a spesific string that its get
    the function simulates slow typing
    """""

    # Not working
    def write_comment(self, comment_text):
        try:
            comment_button = self.driver.find_element_by_link_text('Comment')
            comment_button.click()  # TODO resarch lambidia
        except NoSuchElementException:
            pass
        try:
            comment_box_elem = self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem.send_keys('')
            comment_box_elem.clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 5) / 30))
        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    def post_comment(self, comment_text):
        time.sleep(random.randint(1, 5))  # TODO fix it to a better way to wait

        comment_box_elem = self.write_comment(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
                post_button.click()
                print('clicked post button')
            except NoSuchElementException:
                pass
        time.sleep(3)
        self.driver.refresh()
        if comment_text in self.driver.page_source:  # TODO better way to check if it posted
            return True
        return False


if __name__ == '__main__':
    username = '******'
    password = '******'
    follow_order = "Follow"  # TODO: Enum
    ig_bot = InstagramBot(username, password)
    ig_bot.follow_action('nakash_itay', follow_order)
    hashtag = 'newyork'
    url_hashtag_text = hashtag.format("/explore/tags/", hashtag)
    ig_bot.nav_page(url_hashtag_text)
    ig_bot.nav_page('p/BypKEKXAX6H')
