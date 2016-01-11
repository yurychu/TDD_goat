from unittest import skip
from .base import FunctionalTest


class ItemValidatorTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Эдит заходит на домашнюю страницу и случайно пытается добавить пустой
        # елемент в список.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # Домашняя страница обновляется и появляется сообщение об ошибке ввода
        # пустого значения. Говорится, что список элементов не может быть пустым.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # Она снова пытается добавить элемент в существуюем списке,
        # но уже с каким то текстом.
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1.Buy milk')

        # Ужас в том, что она вновь принимает решение засабмитить пустой элемент в список.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # Но получает аналогичное предупреждение на странице со списком.
        self.check_for_row_in_list_table('1.Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.asssertEqual(error.text, "You can't have an empty list item")

        # Исправляет на корректный текст
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1.Buy milk')
        self.check_for_row_in_list_table('2.Make tea')
        # self.fail("write me!")

