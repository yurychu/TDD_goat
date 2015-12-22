from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Функциональный тест приложения составления списка дел
        # здесь проверяем нашу домашнюю страницу
        self.browser.get('http://localhost:8000')

        # проверяем титул и заголовок страницы утверждением "To-Do"
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        #  1 self.fail('Finish the test')

        # вводим и добавляем элемент списка дел
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # набираем "Buy peacock feathers" в текст - бокс (для хобби рыбалки)
        inputbox.send_keys('Buy peacock feathers')
        # когда нажимаем enter страница обновляется и мы должны увидеть 
        # "1: Buy peacock feathers как элемент списка дел"
        inputbox.send_keys(Keys.ENTER)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1. Buy peacock feathers' for row in rows),
                "New to-do item did not appear in table"
        )

        # дожен все еще присутстововать текст-бокс для добавления других элементов.
        # введем "Use peacock feathers to make a fly"
        self.fail('Finish the test!')

        # страница обновляется снова и мы видим уже оба элемента.

        # возможность сохранить данный список дел с созданием для него уникально ссылки - какой нибудь пояснительный текст для этого эффекта

        # преходим по данной ссылке, после чего должны увидеть этот список дел

        # Если остаемся довольными, то идем спать.

if __name__ == "__main__":
    unittest.main(warnings='ignore')

