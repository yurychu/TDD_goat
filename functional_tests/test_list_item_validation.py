from unittest import skip
from .base import FunctionalTest


class ItemValidatorTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Эдит заходит на домашнюю страницу и случайно пытается добавить пустой
        # елемент в список.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # Домашняя страница обновляется и появляется сообщение об ошибке ввода
        # пустого значения. Говорится, что список элементов не может быть пустым.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # Она снова пытается добавить элемент в существуюем списке,
        # но уже с каким то текстом.
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1.Buy milk')

        # Ужас в том, что она вновь принимает решение засабмитить пустой элемент в список.
        self.get_item_input_box().send_keys('\n')

        # Но получает аналогичное предупреждение на странице со списком.
        self.check_for_row_in_list_table('1.Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
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
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You've already got this in your list")

