from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.pos_page import POSPage
from models.test_models import TestSuite, TestScenario, TestCase, TestStep
from utils.data_reader import DataReader
from utils.logger import setup_logger
from config.settings import Settings
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class TestExecutor:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.settings = Settings()

    def initialize(self, test_data: Dict, headless: bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless, slow_mo=1000)
        self.context = self.browser.new_context()
        self.page = self.browser.new_page(no_viewport=True)

        # Initialize data reader with API-provided test data
        data_reader = DataReader(test_data=test_data)

        # Perform login
        login_page = LoginPage(self.page, data_reader)
        login_page.login()

        # Initialize POS page
        till_name = data_reader.get_value("till_name")
        pos_page = POSPage(self.page, data_reader)
        pos_page.select_till(till_name)

        return pos_page

    def cleanup(self):
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def execute_step(self, pos_page: POSPage, step: TestStep):
        action_map = {
            "select_random_products": lambda: pos_page.select_random_products(),
            "delete_two_products": lambda: pos_page.delete_two_products(),
            "cash_payment_full": lambda: pos_page.cash_payment_full(),
            "upi_payment_full": lambda: pos_page.upi_payment_full(),
            "card_payment_full": lambda: pos_page.card_payment_full(),
            "razor_payment_full": lambda: pos_page.razor_payment_full(),
            "swiggy_payment": lambda: pos_page.swiggy_payment(),
            "zomato_payment": lambda: pos_page.zomato_payment(),
            "online_payment" : lambda :pos_page.online_payment(),
            "cash_payment_partial_dynamic": lambda: pos_page.cash_payment_partial_dynamic(),
            "card_remaining_partial": lambda: pos_page.card_remaining_partial(),
            "upi_remaining_partial": lambda: pos_page.upi_remaining_partial(),
            "razor_remaining_partial": lambda: pos_page.razor_remaining_partial(),
            "sale_type_swiggy": lambda: pos_page.sale_type_swiggy(),
            "sale_type_zomato": lambda: pos_page.sale_type_zomato(),
            "sale_type_online": lambda: pos_page.sale_type_online(),
            "create_customer": lambda: pos_page.create_customer(),
            "product_drawer": lambda: pos_page.product_drawer(),
            "click_element": lambda: pos_page.click_element(step.selector),
            "fill_text": lambda: pos_page.fill_text(step.selector, step.value),
            "verify_text": lambda: pos_page.verify_text(step.selector, step.value),
            "log_out": lambda :pos_page.log_out(),
            "full_sync": lambda :pos_page.full_sync(),
            "press_plus_key": lambda:pos_page.press_plus_key(),
            "press_minus_key":  lambda:pos_page.press_minus_key(),
            "refresh_page": lambda:pos_page.refresh_page(),
            "delect_partial_amount_cash": lambda :pos_page.delect_partial_amount_cash(),
            "hold_parked": lambda: pos_page.hold_parked(),
            "parked_bills": lambda: pos_page.parked_bills(),
            "cancel_product": lambda: pos_page.cancel_product(),
            "parked_bills_discard":lambda :pos_page.parked_bills_discard(),
            "replace_parked_bills":lambda :pos_page.replace_parked_bills(),
            "parked_bills_discard_all":lambda :pos_page.parked_bills_discard_all(),
            "menu_delect":lambda :pos_page.menu_delect(),
            "menu_button":lambda :pos_page.menu_button(),
            "product_sync":lambda :pos_page.product_sync(),
            "product_sync_with_product":lambda :pos_page.product_sync_with_product(),
            "read_present_invoice_number":lambda :pos_page.read_present_invoice_number(),
            "sales_history_two": lambda :pos_page.sales_history_two(),
            "search_invoice_in_sales_history":lambda  :pos_page.search_invoice_in_sales_history(),
            "create_advance_click": lambda :pos_page.create_advance_click(),
            "sales_history_expand": lambda : pos_page.sales_history_expand(),
            "extra_payment_methods": lambda :pos_page.extra_payment_methods(),
            "advance_order": lambda :pos_page.advance_order(),
            "check_customer_alert":lambda :pos_page.check_customer_alert(),
            "close_advance_order":lambda :pos_page.close_advance_order(),
            "handle_product_alert": lambda :pos_page.handle_product_alert(),
            "only_one_product" : lambda :pos_page.only_one_product(),
            "select_tomorrow_date": lambda :pos_page.select_tomorrow_date(),
            "upi_payment_partial_dynamic":lambda :pos_page.upi_payment_partial_dynamic(),
            "total_amount_click": lambda :pos_page.total_amount_click(),
            "change_advance_order_to_sale_order":lambda :pos_page.change_advance_order_to_sale_order(),
            "select_existing_customer": lambda :pos_page.select_existing_customer(),
            "shift_close":lambda :pos_page.shift_close(),
            "manual_discount_amount":lambda :pos_page.manual_discount_amount(),
            "modify_the_order": lambda :pos_page.modify_the_order(),
            "lock_key":lambda :pos_page.lock_key(),
            "remove_and_validate_discount":lambda :pos_page.remove_and_validate_discount(),
            "get_total_amount_to_pay": lambda :pos_page.get_total_amount_to_pay(),
            "apply_manual_discount_percentage":lambda :pos_page.apply_manual_discount_percentage(),
            "sales_history_for_advance":lambda :pos_page.sales_history_for_advance(),
            "process_random_payment": lambda :pos_page.process_random_payment(),
            "store_order_amount":lambda :pos_page.store_order_amount(),
            "validate_sales_amount":lambda :pos_page.validate_sales_amount(),
            "log_out_validation":lambda :pos_page.log_out_validation(),
            "nan_validation":lambda :pos_page.nan_validation(),
            "store_order_id": lambda :pos_page.store_order_id(),
            "coupon_code_without_product":lambda :pos_page.coupon_code_without_product(),
            "coupon_code": lambda :pos_page.coupon_code(),
            "view_stock": lambda :pos_page.view_stock(),
            "over_payment": lambda :pos_page.over_payment(),
            "get_total_amount": lambda :pos_page.get_total_amount(),
            "cash_management_add_cash": lambda :pos_page.cash_management_add_cash(),
            "cash_management_remove_cash": lambda :pos_page.cash_management_remove_cash(),
            "custom_box": lambda :pos_page.custom_box(),
            "custom_boxes": lambda :pos_page.custom_boxes(),
            "Custom_mix_name_changing_dynamically": lambda :pos_page.Custom_mix_name_changing_dynamically(),
            "custom_mix_product_search": lambda :pos_page.custom_mix_product_search(),
            "custom_mix_add_five_products_by_description": lambda :pos_page.custom_mix_add_five_products_by_description(),
            "waiting_order": lambda :pos_page.waiting_order(),
            "reading_values_validation": lambda :pos_page.reading_values_validation(),
            "cash_in": lambda :pos_page.cash_in(),
            "Home_logout": lambda :pos_page.Home_logout(),
            "cash_remove": lambda :pos_page.cash_remove(),
            "custom_mix_qty_change": lambda :pos_page.custom_mix_qty_change(),
            "sand_box": lambda :pos_page.sand_box()





        }

        if step.action not in action_map:
            raise ValueError(f"Unsupported action: {step.action}")

        action_map[step.action]()
        logger.info(f"Executed step: {step.action}")

    def execute_test_case(self, pos_page: POSPage, test_case: TestCase):
        logger.info(f"Executing test case: {test_case.name}")
        for step in test_case.steps:
            try:
                self.execute_step(pos_page, step)
            except Exception as e:
                logger.error(f"Step failed in {test_case.name}: {str(e)}")
                raise

    def execute_test_scenario(self, pos_page: POSPage, scenario: TestScenario):
        logger.info(f"Executing test scenario: {scenario.name}")
        results = []
        for test_case in scenario.test_cases:
            try:
                self.execute_test_case(pos_page, test_case)
                results.append({"test_case": test_case.name, "status": "PASSED"})
            except Exception as e:
                results.append({"test_case": test_case.name, "status": "FAILED", "error": str(e)})
                logger.error(f"Test case {test_case.name} failed: {str(e)}")
        return results

    def execute_test_suite(self, test_suite: TestSuite):
        results = []
        pos_page = None
        try:
            pos_page = self.initialize(test_suite.test_data, headless=False)

            # Apply server details
            base_url = test_suite.server_details.get("base_url", self.settings.BASE_URL)
            logger.info(f"Using base URL: {base_url}")

            # Replace sample data in steps
            for scenario in test_suite.scenarios:
                for test_case in scenario.test_cases:
                    for step in test_case.steps:
                        if step.value and isinstance(step.value, str):
                            for key, value in test_suite.sample_data.items():
                                step.value = step.value.replace(f"{{{{ {key} }}}}", str(value))

            # Execute scenarios
            for scenario in test_suite.scenarios:
                scenario_results = self.execute_test_scenario(pos_page, scenario)
                results.append({"scenario": scenario.name, "test_cases": scenario_results})

        finally:
            self.cleanup()

        return results