from selenium import webdriver
from .base import FunctionalTest
from .home_and_list_pages import HomePage

def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Эдит - залогиненный пользователь
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Ее друг Они тоже на сайте списков
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # Эдит переходит на домашнюю страницу и начинает список дел
        self.browser = edith_browser
        list_page = HomePage(self).start_new_list('Get help')

        # Она помечает опцию "расшарить этот список"
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # список становится расшаренными
        # страница перезагружается и сообщается о расшаривании с Они
        list_page.share_list_with('oniciferous@example.com')

        # Они переходит на этот список
        self.browser = oni_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        # И он видит что там написала Эдит
        self.browser.find_element_by_link_text('Get help').click()

        # И он может добавить туда еще что то
        list_page.add_new_item('Hi Edith!')

        # Когда Эдит обновляет свою страницу - она видит, что добавил Они
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi Edith!', 2)
