from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Функциональный тест приложения составления списка дел
        # здесь проверяем нашу домашнюю страницу
        self.browser.get(self.live_server_url)

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

        # страница обновляется, должны увидеть введенный элемент

        self.check_for_row_in_list_table('1.Buy peacock feathers')

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1.Buy peacock feathers', [row.text for row in rows])

        # дожен все еще присутстововать текст-бокс для добавления других элементов.
        # введем "Use peacock feathers to make a fly"
        # 2 self.fail('Finish the test!')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # страница обновляется снова и мы видим уже оба элемента.

        self.check_for_row_in_list_table('1.Buy peacock feathers')
        self.check_for_row_in_list_table('2.Use peacock feathers to make a fly')

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1.Buy peacock feathers', [row.text for row in rows])
        #self.assertIn('2.Use peacock feathers to make a fly', [row.text for row in rows])

        # возможность сохранить данный список дел с созданием для него уникально ссылки - какой нибудь пояснительный текст для этого эффекта
        self.fail('Finish the test!')
        
        # преходим по данной ссылке, после чего должны увидеть этот список дел

        # Если остаемся довольными, то идем спать.

if __name__ == "__main__":
    unittest.main(warnings='ignore')

