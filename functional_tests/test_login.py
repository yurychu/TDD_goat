import time

from .base import FunctionalTest

from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find window')

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}.Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('edith@mockmyid.com', navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn('edith@mockmyid.com', navbar.text)

    def test_login_with_persona(self):
        # Эдит заходит на наш замечательный сайт со списками
        # и впервые замечает сслыку "Sign in"
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # Открывается окно логина Mozilla Persona
        self.switch_to_new_window("Mozilla Persona")

        # Эдит входит с адресом своей почты
        ## Используем mockmyid.com для теста
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('edith@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # Окно Persona закрывается
        self.switch_to_new_window('To-Do')

        # Она может увидеть, что она зашла
        self.wait_to_be_logged_in()

        # Обновление страницы, реальная ссесия должна сохраниться
        # и что не произошло выхода со страницы
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # Испугавшись новой фичи, жмет logout
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # Статус logged out - должен сохраняться после рефреша страницы
        self.browser.refresh()
        self.wait_to_be_logged_out()

