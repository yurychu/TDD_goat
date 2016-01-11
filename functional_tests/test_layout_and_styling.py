from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Эдит заходит на домашнюю страницу
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Она видит строку ввода красиво расположенную по центру
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

