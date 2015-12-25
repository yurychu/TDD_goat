import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    

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
        
        # добавили запоминалку ссылки на личный список дел пользователя
        # для проверки в конце теста
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1.Buy peacock feathers')

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

        # Новый пользователь, Френсис заходит на сайт
        ## Нам нужно использовать новую сессию, что бы быть уверенными, что
        ## информация от Эдит не повлияет в виде куки и тд
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Френсис посещает домашнуюю страницу сайта.
        # Здесь он не должен увидеть список Эдит.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Френсис начинает вводить элементы своего списка дел
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Френсис так же получает уникальную ссылку на свой список
        # она должна отличаться от ссылки Эдит
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # И опять таки нету никаких следов списка Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Если эти оба останутся довольными, то идем спать.

    def test_layout_and_styling(self):
        # Эдит заходит на домашнюю страницу
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Она видит строку ввода красиво расположенной по центру
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
                )
        # Она начинает создавать новый список дел и при добавлени последующих
        # так же видит строку ввода, расположенную по центру
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=5
                )

if __name__ == "__main__":
    unittest.main(warnings='ignore')

