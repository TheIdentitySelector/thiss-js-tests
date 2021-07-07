from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import EdgeOptions, Edge
from datetime import datetime


import unittest
import time
import json
import warnings
import argparse


class SeamlessTests(unittest.TestCase):

    def setUp(self):

        if(args.browser.lower() == 'firefox'):
            options = webdriver.FirefoxOptions()

            if (args.headless.lower() == "true"):
                options.headless = True

            if(args.mobile.lower() == "true"):
                user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", user_agent)
                self.driver = webdriver.Firefox(profile, options=options)

            if (args.mobile.lower() == "true"):
                self.driver.set_window_size(360, 640)
            else:
                self.driver = webdriver.Firefox(options=options)


        elif(args.browser.lower() == 'edge'):
            options = EdgeOptions()
            options.use_chromium = True
            options.set_capability("platform", "LINUX")
            options.binary_location = args.binary
            if(args.headless.lower() == "true"):
                options.add_argument("--headless")
            if (args.mobile.lower() == "true"):
                mobile_emulation = {"deviceName": args.device}
                options.add_experimental_option("mobileEmulation", mobile_emulation)

            self.driver = Edge(options=options)

        elif(args.browser.lower() == 'chrome'):
            options = webdriver.ChromeOptions()
            if (args.headless.lower() == "true"):
                options.add_argument("--headless")
            if(args.mobile.lower() == "true"):
                mobile_emulation = {"deviceName": args.device}
                options.add_experimental_option("mobileEmulation", mobile_emulation)

            self.driver = webdriver.Chrome(options=options)


    def tearDown(self):
        self.driver.close()
        current_time = datetime.now()
        print("Test ended at: ", current_time)

    @classmethod
    def setUpClass(cls):
        global data
        with open(args.json, "r") as f:
            data = json.load(f)

        current_time = datetime.now()
        print("Test started at: ", current_time)

    def test_selecting_institution(self):  # 1A
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["selecting_institution"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # typing bme
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if args.browser.lower() == 'chrome':
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["selecting_institution"]["src"])

        # selecting bme institutionischrome = False
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["selecting_institution"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath(
            '//a[@data-href="' + data["selecting_institution"]["url"] + '"]'))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text

        try:
            self.assertIn(data["selecting_institution"]["name"], button_text)
        except:
            warnings.warn("Institution name is not on blue button")

    def test_too_many_results(self):  # 1B
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["too_many_results"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # typing uni
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["too_many_results"]["src"])

        # checking search list appears
        wait.until(EC.presence_of_element_located((By.ID, "ds-search-list")))
        wait.until(EC.text_to_be_present_in_element((By.ID, "ds-search-list"), "keep typing to refine your search"))

        # checking if the excepted text appears
        refine_text = browser.find_element_by_id("ds-search-list").text
        self.assertIn("keep typing to refine your search", refine_text)

    def test_typing_delays(self):  # 1C, time measuring, this test currently fails
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["typing_delays"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # type in "uni", it should give thousand of results
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["typing_delays"]["src"])

        # if the search takes more than 1 seconds, yield a warning
        try:
            WebDriverWait(browser, 1).until(
                EC.text_to_be_present_in_element((By.ID, "ds-search-list"), "keep typing to refine your search"))
        except:
            warnings.warn("It took more than 1 seconds")
        else:
            print("It took less than 1 seconds")

    def test_show_all_matches(self):  # 1D
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["show_all_matches"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # search for "london"
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["show_all_matches"]["src"])

        # pressing the show all button (also checking if present) and waiting for list to appear
        wait.until(EC.presence_of_element_located((By.ID, "showall")))
        assert browser.find_element_by_id("showall")
        browser.find_element_by_id("showall").click()
        wait.until(EC.text_to_be_present_in_element((By.ID, "ds-search-list"), "London Business School"))

        # checking if the list contains more than 10 results
        self.assertTrue(len(browser.find_elements_by_xpath
                            ("//a[@class='institution identityprovider bts-dynamic-item']")) > 10)  # len return 36 not 37, one less, check!

    def test_remember_selection1(self):  # 2A1
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["remember_selection"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["remember_selection"]["src"])

        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["remember_selection"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[@data-href="' + data["remember_selection"]["url"] + '"]'))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text

        self.assertIn(data["remember_selection"]["name"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        wait.until((EC.presence_of_element_located((By.ID, "savedchoices"))))
        wait.until(EC.text_to_be_present_in_element((By.ID, "savedchoices"), data["remember_selection"]["name"]))
        institution_text = browser.find_element_by_id("savedchoices").text
        self.assertIn(data["remember_selection"]["name"], institution_text)

    def test_remember_selection2(self):  # 2A2
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["remember_selection"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["remember_selection"]["src"])

        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["remember_selection"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//a[@data-href="' + data["remember_selection"]["url"] + '"]'))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text

        self.assertIn(data["remember_selection"]["name"], button_text)
        browser.switch_to.default_content()
        browser.switch_to.frame(iframe)
        browser.find_element_by_id("dsbutton").click()
        browser.switch_to.default_content()

        wait.until(EC.presence_of_element_located((By.ID, "savedchoices")))
        wait.until(EC.text_to_be_present_in_element((By.ID, "savedchoices"), data["remember_selection"]["name"]))
        institution_text = browser.find_element_by_id("savedchoices").text
        self.assertIn(data["remember_selection"]["name"], institution_text)

    def test_delete_selection(self):  # 2B
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["delete_selection"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # searching and choosing elte
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["delete_selection"]["src"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["delete_selection"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[@data-href="' + data["delete_selection"]["url"] + '"]'))

        # check if elte is remembered
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["delete_selection"]["name"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        # deleting elte
        wait.until(EC.element_to_be_clickable((By.ID, "edit_button")))
        browser.find_element_by_id("edit_button").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//i[@class="institution-remove remove top-right"]')))
        browser.find_element_by_xpath('//i[@class="institution-remove remove top-right"]').click()

        # checking if elte institution name is not on the blue button,
        # and that the default "Find Your Institution" is there
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        no_inst_text = browser.find_element_by_id("search").text
        self.assertIn("Find Your Institution", no_inst_text)
        self.assertNotIn(data["delete_selection"]["name"], no_inst_text)

    def test_add_more_selection(self):  # 2C1
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["add_more_selection"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # searching and choosing elte
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["add_more_selection"]["src"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_more_selection"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//a[@data-href="' + data["add_more_selection"]["url"] + '"]'))

        # check if elte is added
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["add_more_selection"]["name"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        # adding 2nd inst., bme
        wait.until(EC.element_to_be_clickable((By.ID, "add_button")))
        browser.find_element_by_id("add_button").click()
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        browser.find_element_by_id("searchinput").send_keys(data["add_more_selection"]["src2"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_more_selection"]["url2"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[@data-href="' + data["add_more_selection"]["url2"] + '"]'))

        # check if both are remembered
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        browser.find_element_by_class_name("visible").click()
        wait.until(EC.text_to_be_present_in_element((By.ID, "savedchoices"), data["add_more_selection"]["name"]))
        saved_choices = browser.find_element_by_id("savedchoices").text
        self.assertIn(data["add_more_selection"]["name"], saved_choices)
        self.assertIn(data["add_more_selection"]["name2"], saved_choices)

    def test_add_4th_selection(self):  # 2C2
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["add_4th_selection"]["base_url"])
        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # adding first institutin, elte
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["add_4th_selection"]["src"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_4th_selection"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//a[@data-href="' + data["add_4th_selection"]["url"] + '"]'))

        # checking that elte is added
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["add_4th_selection"]["name"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        # adding second inst., bme
        wait.until(EC.element_to_be_clickable((By.ID, "add_button")))
        browser.find_element_by_id("add_button").click()
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        browser.find_element_by_id("searchinput").send_keys(data["add_4th_selection"]["src2"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_4th_selection"]["url2"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[@data-href="' + data["add_4th_selection"]["url2"] + '"]'))

        # checking if bme is added
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["add_4th_selection"]["name2"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        # adding 3rd inst., sztaki
        wait.until(EC.element_to_be_clickable((By.ID, "add_button")))
        browser.find_element_by_id("add_button").click()
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        browser.find_element_by_id("searchinput").send_keys(data["add_4th_selection"]["src3"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_4th_selection"]["url3"] + '"]')))
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//a[@data-href="' + data["add_4th_selection"]["url3"] + '"]'))

        # checkinf if sztaki is added
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["add_4th_selection"]["name3"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()

        # check that all 3 is remembered
        wait.until(EC.text_to_be_present_in_element((By.ID, "savedchoices"), data["add_4th_selection"]["name"]))
        saved_choices = browser.find_element_by_id("savedchoices").text
        self.assertIn(data["add_4th_selection"]["name"], saved_choices)
        self.assertIn(data["add_4th_selection"]["name2"], saved_choices)
        self.assertIn(data["add_4th_selection"]["name3"], saved_choices)

        # the browser local storage remembers 3 institutions, we add a 4th one and except that,
        # the first (elte) will no longer be remembered
        wait.until(EC.element_to_be_clickable((By.ID, "add_button")))
        browser.find_element_by_id("add_button").click()
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        browser.find_element_by_id("searchinput").send_keys(data["add_4th_selection"]["src4"])
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["add_4th_selection"]["url4"] + '"]')))
        browser.execute_script("arguments[0].click();",
                               browser.find_element_by_xpath('//a[@data-href="' + data["add_4th_selection"]["url4"] + '"]'))

        # lastly, we check if geant is added, the excepted 3 is stored and elte is no longer remembered
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text
        self.assertIn(data["add_4th_selection"]["name4"], button_text)
        browser.switch_to.default_content()
        browser.find_element_by_class_name("visible").click()
        time.sleep(1)  # without these the chrome tests fail

        wait.until(EC.text_to_be_present_in_element((By.ID, "savedchoices"), data["add_4th_selection"]["name4"]))
        saved_choices = browser.find_element_by_id("savedchoices").text
        self.assertIn(data["add_4th_selection"]["name2"], saved_choices)
        self.assertIn(data["add_4th_selection"]["name3"], saved_choices)
        self.assertIn(data["add_4th_selection"]["name4"], saved_choices)
        self.assertNotIn(data["add_4th_selection"]["name"], saved_choices)

    def test_dont_remember(self):  # 2D
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["dont_remember"]["base_url"])

        time.sleep(1)
        browser.find_element_by_class_name("visible").click()

        # typing elte
        wait.until(EC.element_to_be_clickable((By.ID, "searchinput")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("searchinput").send_keys(data["dont_remember"]["src"])
        # ticking the "do not remember" checkbox
        browser.find_element_by_class_name("custom-control-label").click()

        # adding elte instituiton
        wait.until(EC.element_to_be_clickable((By.ID, "ds-search-list")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-href="' + data["dont_remember"]["url"] + '"]')))
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[@data-href="' + data["dont_remember"]["url"] + '"]'))

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "visible")))
        iframe = browser.find_element_by_xpath(("//iframe[@class='visible']"))
        browser.switch_to.frame(iframe)
        button_text = browser.find_element_by_id(("idpbutton")).text

        # checking if elte institution name is not on the blue button,
        # and that the default "Access through your institution" is there
        self.assertIn("Access through your institution", button_text)
        self.assertNotIn(data["dont_remember"]["name"], button_text)

    def test_learn_more(self):  # 3A, learn more button only appears if no isntitution is remembered
        browser = self.driver
        wait = WebDriverWait(browser, 5)

        browser.get(data["learn_more"]["base_url"])
        time.sleep(1)

        # clicking on the blue button and the learn more text
        browser.find_element_by_class_name("visible").click()
        wait.until(EC.element_to_be_clickable((By.ID, "learn-more-trigger")))
        if(args.browser.lower() == 'chrome'):
            time.sleep(1)  # without these the chrome tests fail
        browser.find_element_by_id("learn-more-trigger").click()

        # check if the text appears, also checking if the link to Additional Privacy Information redirect to the correct url
        wait.until(EC.presence_of_element_located((By.ID, "learn-more-banner")))
        learn_more_text = browser.find_element_by_id("learn-more-banner").text
        self.assertIn(data["learn_more"]["learn_more_text"], learn_more_text)
        browser.find_element_by_xpath('//a[contains(@href,"' + data["learn_more"]["url"] + '")]').click()  # additional privacy information button
        self.assertEqual(data["learn_more"]["url"], browser.current_url)


def main():
    global args

    parser = argparse.ArgumentParser(description='Seamless tests')
    parser.add_argument('--json', dest='json', type=str, help='The JSON file containing the inputs', required=True)
    parser.add_argument('--browser', dest='browser', type=str, help='The browser to run the tests with', required=True)
    parser.add_argument('--headless', dest='headless', type=str, help='Run the tests in headless mode', default="True")
    parser.add_argument('--mobile', dest='mobile', type=str, help='Run the test in mobile mode', default="False")
    parser.add_argument('--device', dest='device', type=str, help='Device for mobile mode testing, see README.md for device list', default="iPhone X")
    parser.add_argument('--binary', dest='binary', type=str, help='Location of binary file for MSEdge tests under Linux')
    parser.add_argument('remaining', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.browser == 'edge' and args.binary is None:
        parser.error("Edge tests require binary path")

    unittest.main(argv=args.remaining)


if __name__ == '__main__':
    main()