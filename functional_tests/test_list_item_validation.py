from unittest import skip
from .base import FunctionalTest


class ItemValidatorTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Эдит заходит на домашнюю страницу и случайно пытается добавить пустой
        # елемент в список.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # Домашняя страница обновляется и появляется сообщение об ошибке ввода
        # пустого значения. Говорится, что список элементов не может быть пустым.
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # Она снова пытается добавить элемент в существуюем списке,
        # но уже с каким то текстом.
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1.Buy milk')

        # Ужас в том, что она вновь принимает решение засабмитить пустой элемент в список.
        self.get_item_input_box().send_keys('\n')

        # Но получает аналогичное предупреждение на странице со списком.
        self.check_for_row_in_list_table('1.Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # Исправляет на корректный текст
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1.Buy milk')
        self.check_for_row_in_list_table('2.Make tea')
        # self.fail("write me!")

    def test_cannot_add_duplicate_items(self):
        # Эдит заходит на домашнюю страницу и начинает новый список
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1.Buy wellies')

        # Она случайно пытается добавить такую же задачу еще раз
        self.get_item_input_box().send_keys('Buy wellies\n')

        # Она видит подсказку об ошибке
        self.check_for_row_in_list_table('1.Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_errors_messages_are_cleared_on_input(self):
        # Эдит начинает создавать новый список добавлением пустого элемета
        # Должна быть вызвана ошибка валидации
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # Она начинает печатать в поле ввода, что бы устранить ошибку
        self.get_item_input_box().send_keys('a')

        # Она в восторге, когда сообщение об ошибке исчезает
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())

