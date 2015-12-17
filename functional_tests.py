from selenium import webdriver
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
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        # вводим и добавляем элемент списка дел
        # набираем "Buy peacock feathers" в текст - бокс (для хобби рыбалки)

        # когда нажимаем enter страница обновляется и мы должны увидеть 
        # "1: Buy peacock feathers как элемент списка дел"

        # дожен все еще присутстововать текст-бокс для добавления других элементов.
        # введем "Use peacock feathers to make a fly"

        # страница обновляется снова и мы видим уже оба элемента.

        # возможность сохранить данный список дел с созданием для него уникально ссылки - какой нибудь пояснительный текст для этого эффекта

        # преходим по данной ссылке, после чего должны увидеть этот список дел

        # Если остаемся довольными, то идем спать.

if __name__ == "__main__":
    unittest.main(warnings='ignore')

