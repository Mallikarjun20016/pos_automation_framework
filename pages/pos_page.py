from os import name

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
import random
import time
from faker import Faker
import  re

from pages.login_page import LoginPage
from utils.data_reader import DataReader
import math
import logging
import string
from datetime import datetime
from datetime import datetime, timedelta
fake = Faker()
logger = logging.getLogger(__name__)

class POSPage(BasePage):
    def __init__(self, page, data_reader: DataReader):
        super().__init__(page)
        self.order_amounts = None
        self.data_reader = data_reader
        self.order_ids = []
        self.context = page.context
        self.order_count = 0
        self.cash_order_totals = []

    def select_till(self, till_name):
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        import logging
        import time

        logger = logging.getLogger(__name__)

        try:
            # Log start time
            start_time = time.time()
            logger.info(f"Starting till selection: {till_name}")

            # Click the till
            xpath_till = f"//span[text()='{till_name}']"
            self.click_element(xpath_till)
            logger.info(f"Clicked till: {till_name}")

            # Check for loading spinner (optional, since it disappeared quickly)
            try:
                self.page.wait_for_selector("//div[contains(@class, 'loading-spinner') or contains(text(), 'Loading')]",
                                            state="hidden", timeout=30000)
                logger.info("Loading spinner disappeared")
            except PlaywrightTimeoutError:
                logger.info("No loading spinner detected or it did not disappear within 30 seconds")

            # Dynamically wait for the Next button with polling
            max_wait_time = 300  # Maximum wait time in seconds (5 minutes), adjustable
            poll_interval = 5  # Check every 5 seconds
            elapsed_time = 0

            while elapsed_time < max_wait_time:
                try:
                    if self.page.locator("//span[text()='Next']").is_visible():
                        logger.info("Next button is visible")
                        break
                except:
                    pass  # Ignore exceptions during polling
                time.sleep(poll_interval)
                elapsed_time += poll_interval
                logger.debug(f"Waiting for Next button... {elapsed_time} seconds elapsed")

            if elapsed_time >= max_wait_time:
                logger.error(
                    f"Failed to select till: {till_name}. Next button not visible after {max_wait_time} seconds")
                dom_content = self.page.content()[:1000]
                logger.debug(f"DOM content: {dom_content}")
                self.page.screenshot(path="till_selection_error.png")
                logger.info("Screenshot saved as till_selection_error.png")
                raise Exception(
                    f"Till selection timeout: Next button not visible for till {till_name} after {max_wait_time} seconds")

            # Click the Next button
            self.click_element("//span[text()='Next']")
            logger.info("Clicked Next button")

            # Log total time taken
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"Till selection completed in {duration:.2f} seconds")

        except Exception as e:
            logger.error(f"Error in select_till: {e}")
            self.page.screenshot(path="error_screenshot.png")
            logger.info("Screenshot saved as error_screenshot.png")
            raise



    def waiting_order(self):
        logger.info("Pausing for 3 minutes as per requirement...")
        time.sleep(180)  # Pause for 300 seconds (5 minutes)
        logger.info("Resuming test execution after 3-minute pause.")


    def select_random_products(self):
        product_codes = self.data_reader.get_value("product_codes", [])
        selected = random.sample(product_codes, min(1, len(product_codes)))

        for code in selected:
            self.fill_text("//input[@id='sm-product-search']", code)
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)
        logger.info(f"Selected products: {selected}")

    def press_plus_key(self,times:int = 3):
        for _ in range(times):
            self.page.keyboard.press("+")
        logger.info("products should be  added")


    def press_minus_key(self,times:int = 3):
        for _ in range(times):
            self.page.keyboard.press("-")
            logger.info("products should be delected")


    def refresh_page(self):
        self.page.reload()

    def delect_partial_amount_cash(self):
        self.click_element('//img[@style="height: 15px; width: 15px; cursor: pointer; margin-left: 1vw; position: absolute; right: 5px; top: 15%;"]')





    def product_drawer(self):
        self.click_element("//button[@id='sm-product-drawer']")
        self.click_element("(//span[contains(text(),'ADD')])[2]")
        self.click_element("//button[@id='sm-product-drawer']")
        self.click_element("(//span[contains(text(),'ADD')])[1]")
        self.click_element("//button[@id='sm-product-drawer']")
        self.click_element("(//span[contains(text(),'ADD')])[3]")
        logger.info("Added products from drawer")

    def delete_two_products(self):
        self.click_element('(//img[contains(@id,"sm-product-delete")])[2]')
        logger.info("Deleted two products")

    def cash_payment_full(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='Cash']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed full cash payment")


    def upi_payment_full(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='UPI']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed full UPI payment")

    def razor_payment_full(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='Razor Pay']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed full Razor Pay payment")

    def card_payment_full(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='Card']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed full card payment")

    def swiggy_payment(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("(//span[contains(text(),'Swiggy')])[3]")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed Swiggy payment")

    def zomato_payment(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("(//span[contains(text(),'Zomato')])[3]")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed Zomato payment")

    def online_payment(self):
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("(//span[contains(text(),'Online')])[2]")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed Online payment")

    def cash_payment_partial_dynamic(self):
        total_amount_text = self.page.inner_text("//p[text()='Total Amount To Pay']/following-sibling::p")
        total_amount = float(total_amount_text.replace("₹", "").strip())

        if total_amount > 1:
            partial_amount = random.randint(1, math.floor(total_amount - 1))
        else:
            partial_amount = 1

        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='Cash']")
        self.fill_text("//input[@placeholder='Enter Amount']", str(partial_amount))
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info(f"Processed partial cash payment: {partial_amount}")

    def card_remaining_partial(self):
        self.click_element("//span[text()='Card']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed remaining card payment")

    def upi_remaining_partial(self):
        self.click_element("//span[text()='UPI']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed remaining UPI payment")

    def razor_remaining_partial(self):
        self.click_element("//span[text()='Razor Pay']")
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info("Processed remaining Razor Pay payment")

    def sale_type_swiggy(self):
        self.click_element("//span[text()='Walkin']")
        self.click_element("//div[@style='background-color: rgb(142, 172, 205); margin-bottom: 1.5vh; height: 14vh; display: flex; justify-content: center; align-items: center; border-radius: 10px;']//span[text()='Swiggy']")
        logger.info("Set sale type to Swiggy")

    def sale_type_zomato(self):
        self.click_element("//span[text()='Walkin']")
        self.click_element(
            "//div[@style='background-color: rgb(222, 229, 212); margin-bottom: 1.5vh; height: 14vh; display: flex; justify-content: center; align-items: center; border-radius: 10px;']//span[text()='Zomato']")
        logger.info("Set sale type to Zomato")

    def sale_type_online(self):
        self.click_element("//span[text()='Walkin']")
        self.click_element("(//div[contains(@class, 'productName')])[4]")
        logger.info("Set sale type to Online")

    # def create_customer(self):
    #     name = fake.name()
    #     self.click_element("//input[@id='sm-customer-search']")
    #     self.click_element("//span[text()='Add Customer']")
    #     self.fill_text("//input[@placeholder='First Name']", name)
    #     self.click_element("//span[text()='Create new Customer']")
    #     logger.info(f"Created customer: {name}")

    def create_customer(self):
        name = fake.name()
        self.last_created_customer = name  # Store for later use

        self.click_element("//input[@id='sm-customer-search']")
        self.click_element("//span[text()='Add Customer']")
        self.fill_text("//input[@placeholder='First Name']", name)
        self.click_element("//span[text()='Create new Customer']")

        logger.info(f"Created customer: {name}")

    def select_existing_customer(self):
        name = getattr(self, "last_created_customer", None)
        if not name:
            raise ValueError("No customer name stored. Please create a customer first.")

        self.click_element("//input[@id='sm-customer-search']")
        self.click_element("(//input[contains(@id,'sm-product-search')])[2]")
        self.fill_text("(//input[contains(@id,'sm-product-search')])[2]", name)
        self.click_element('//p[@style="margin-bottom: 0px; color: rgb(15, 7, 24); font-size: 1.25em; font-weight: 500; position: relative; text-align: left;"]')
        # self.click_element(f"//span[contains(text(), '{name}')]")


        logger.info(f"Selected existing customer: {name}")

    def log_out(self):
        self.click_element('//img[@style="padding-left: 1rem; height: 2vw;"]')
        self.click_element("//span[text() = 'Logout']")
        self.click_element("//span[text() = 'Next']")
        self.click_element("//span[text() = 'Next']")
        self.click_element("//span[text() = 'Close Shift']")
        logger.info(f"log_out: {name}")

    def  menu_button(self):
        self.click_element("(//div[contains(@class ,'ant-col ant-col-1')])[1]")

    def full_sync(self):
        self.click_element("//span[text() = 'Full Sync']")
        logger.info("full_sync")

    def menu_delect(self):
        self.click_element('//img[@style="margin-left: auto; padding-top: 2vh; cursor: pointer; width: 1.5vw;"]')

    def product_sync(self):
        self.click_element("//span[text() = 'Product Sync']")
        logger.info("product_sync")

    def product_sync_with_product(self):
        self.click_element("//span[text() = 'Product Sync']")
        self.click_element("//span[text() =  'Yes']")
        logger.info("products_sync")

    def unlink(self):
        self.click_element("//span[text()  =  'Unlink Till']")
        self.click_element("//span[text() = 'Next']")
        self.click_element("//span[text() = 'Next']")
        self.click_element("//span[text() = 'Close Shift']")
        logger.info("Unlink")

    def hold_parked(self):
        self.click_element('//span[text()="Hold"]')
        self.click_element('//span[text()="Yes"]')
        logger.info(f"Clicked Hold")

    def cancel_product(self):
        self.click_element('//span[text()="Cancel"]')
        self.click_element('//span[text()="Yes"]')
        logger.info(f"Clicked Cancel Button: Cancel")

    def parked_bills(self):
        # Click on Parked Bills menu
        self.click_element('//span[text()="Parked Bills"]')

        # Fetch all parked bill arrows
        try:
            right_arrows = self.page.query_selector_all('//span[@style="color: rgb(146, 144, 152);"]')

            if right_arrows and len(right_arrows) >= 2:
                right_arrows[1].click()
                logger.info("Clicked on 2nd parked bill.")
            elif right_arrows and len(right_arrows) == 1:
                right_arrows[0].click()
                logger.info("Only 1 parked bill available. Clicked on the 1st one.")
            else:
                logger.warning("No parked bills found.")
                return

            # Click the retrieve button
            self.click_element('//p[@id="sm-parked-bill-retrieve"]')
            logger.info("Clicked on Retrieve Sale.")

        except Exception as e:
            logger.error(f"Error while retrieving parked bill: {e}")

    def parked_bills_discard(self):
        # Click on Parked Bills menu
        self.click_element('//span[text()="Parked Bills"]')

        # Fetch all parked bill arrows
        try:
            right_arrows = self.page.query_selector_all('//span[@style="color: rgb(146, 144, 152);"]')

            if right_arrows and len(right_arrows) >= 2:
                right_arrows[1].click()
                logger.info("Clicked on 2nd parked bill.")
            elif right_arrows and len(right_arrows) == 1:
                right_arrows[0].click()
                logger.info("Only 1 parked bill available. Clicked on the 1st one.")
            else:
                logger.warning("No parked bills found.")
                return

            # Click the retrieve button
            self.click_element('//p[@id="sm-parked-bill-discard"]')
            self.click_element("//span[text() ='OK']")
            self.click_element("//img[@id= 'sm-parked-bill-back']")
            logger.info("Clicked discard Sale.")



        except Exception as e:
            logger.error(f"Error while discard parked bill: {e}")

    def parked_bills_discard_all(self):
        # Click on Parked Bills menu
        self.click_element('//span[text()="Parked Bills"]')
        self.click_element("//span[@id= 'sm-parked-bill-expand']")
        self.click_element('//p[@id="sm-parked-bill-discard"]')
        self.click_element("//span[text()='OK']")
        self.click_element("//img[@id='sm-parked-bill-back']")
        logger.info("Discarded one parked bill.")

    def replace_parked_bills(self):
        # Click on Parked Bills menu
        self.click_element('//span[text()="Parked Bills"]')

        # Fetch all parked bill arrows
        try:
            right_arrows = self.page.query_selector_all('//span[@style="color: rgb(146, 144, 152);"]')

            if right_arrows and len(right_arrows) >= 2:
                right_arrows[1].click()
                logger.info("Clicked on 2nd parked bill.")
            elif right_arrows and len(right_arrows) == 1:
                right_arrows[0].click()
                logger.info("Only 1 parked bill available. Clicked on the 1st one.")
            else:
                logger.warning("No parked bills found.")
                return

            # Click the retrieve button
            self.click_element('//p[@id="sm-parked-bill-retrieve"]')
            self.click_element("//span[text() ='Yes']")
            logger.info("Clicked replace Sale.")

        except Exception as e:
            logger.error(f"Error while retrieving parked bill: {e}")


    def unlink_when_orders_in_PB(self):
        self.click_element("//span[text()  =  'Unlink Till']")
        self.click_element('//img[@style="margin-left: auto; padding-top: 2vh; cursor: pointer; width: 1.5vw;"]')
        self.click_element('//span[text()="Parked Bills"]')

        # Fetch all parked bill arrows
        try:
            right_arrows = self.page.query_selector_all('//span[@style="color: rgb(146, 144, 152);"]')

            if right_arrows and len(right_arrows) >= 2:
                right_arrows[1].click()
                logger.info("Clicked on 2nd parked bill.")
            elif right_arrows and len(right_arrows) == 1:
                right_arrows[0].click()
                logger.info("Only 1 parked bill available. Clicked on the 1st one.")
            else:
                logger.warning("No parked bills found.")
                return

            # Click the retrieve button
            self.click_element('//p[@id="sm-parked-bill-retrieve"]')
            logger.info("Clicked on Retrieve Sale.")

        except Exception as e:
            logger.error(f"Error while retrieving parked bill: {e}")

    def read_present_invoice_number(self):
        self.click_element('//span[text()="Invoice"]')
        self.click_element('//span[text()="Advance"]')

        invoice_locator = self.page.locator("//span[contains(text(),'Invoice No:')]")
        self.page.wait_for_selector("//span[contains(text(),'Invoice No:')]")
        full_text = invoice_locator.inner_text().strip()
        invoice_number = full_text.replace("Invoice No:", "").strip()
        print(f"Present Invoice Number: {invoice_number}")

        self.invoice_no = invoice_number

        return invoice_number

    def sales_history_two(self):

        invoice_number = self.invoice_no

        self.click_element('//span[text()="Sales History"]')
        self.page.wait_for_timeout(9000)

        search_input = self.page.locator('//input[@placeholder="Search for Customers/Document Number/Contact"]')
        search_input.fill(invoice_number)
        search_input.press("Enter")
        self.page.wait_for_timeout(2000)

    def search_invoice_in_sales_history(self):
        # This function becomes unnecessary if sales_history_two uses self.invoice_no
        self.sales_history_two()

    def sales_history_expand(self):
        self.click_element("//span[@id= 'sm-salesHistory-expand']")
        self.click_element("//p[text()='Retrieve Sale']")

    def extra_payment_methods(self):
        self.click_element('//span[text()="..."]')
        self.click_element('//span[text()="Complete Order"]')
        logger.info("Completed order: Done")

    def create_advance_click(self):
        self.click_element('//div[text()="Create Advance"]')
        logger.info("advance: clicked")

    def advance_order(self):
        self.click_element('//span[text()="Invoice"]')
        self.click_element('//span[text()="Advance"]')
        logger.info("Clicked on Invoice > Advance")

    def check_customer_alert(self) -> bool:
        """Handle 'Customer not selected' alert."""
        try:
            locator = self.page.locator('//div[@class="ant-message-custom-content ant-message-warning"]/span')
            locator.wait_for(timeout=3000)
            alert_text = locator.inner_text()
            print(f" ALERT DISPLAYED: {alert_text}")  # Printed to console
            logger.warning(f"Alert shown: {alert_text}")  # Logged
            return True
        except TimeoutError:
            logger.info(" No customer alert appeared.")
            return False

    def close_advance_order(self):
        self.click_element("//span[@class = 'anticon anticon-close ant-modal-close-icon']")

    def handle_product_alert(page: Page):
        try:
            # Wait for the alert message to appear (max 5 seconds)
            alert_locator = page.locator("div.ant-message-custom-content.ant-message-error span")
            alert_locator.wait_for(timeout=5000)

            # Extract and print the alert message text
            alert_text = alert_locator.text_content()
            print(f"[PRODUCT ALERT] {alert_text.strip()}")

        except Exception as e:
            print("[PRODUCT ALERT] No alert message appeared or timed out.")

    def only_one_product(self):
        self.click_element("//button[@id='sm-product-drawer']")
        self.click_element("(//span[contains(text(),'ADD')])[2]")

    def select_tomorrow_date(self):
        # Step 1: Click the calendar icon to open the picker
        self.click_element('//span[@aria-label="calendar"]')
        self.click_element('//input[@placeholder="Select date"]')

        # Step 2: Calculate tomorrow's day number
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow_day = str(tomorrow.day)

        # Step 3: Click the date (e.g., '6' for May 6)
        self.click_element(f"//div[contains(@class,'ant-picker-cell-inner') and text()='{tomorrow_day}']")

        # Step 4: Click "Ok" to confirm
        self.click_element("//span[text()='Ok']")

        print(f"[CALENDAR] Selected tomorrow's date: {tomorrow.strftime('%Y-%m-%d')}")


    def upi_payment_partial_dynamic(self):
        total_amount_text = self.page.inner_text("//p[text()='Total Amount To Pay']/following-sibling::p")
        total_amount = float(total_amount_text.replace("₹", "").strip())

        if total_amount > 1:
            partial_amount = random.randint(1, math.floor(total_amount - 1))
        else:
            partial_amount = 1

        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='UPI']")
        self.fill_text("//input[@placeholder='Enter Amount']", str(partial_amount))
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info(f"Processed partial cash payment: {partial_amount}")

    def total_amount_click(self):
        self.click_element("//p[text()='Total Amount To Pay']")

    def  change_advance_order_to_sale_order(self):
        self.click_element('//span[text()="Advance"]')
        self.click_element('//span[text()="Invoice"]')

    def shift_close(self):
        logger.info("Starting login inside shift_close()")
        self.click_element('//div[@style="padding-top: 1em;"]')

        logger.info("Initiating login after shift close")
        login_page = LoginPage(self.page, self.data_reader)
        login_page.login_without_url()
        self.click_element('//span[text()="Next"]')
        logger.info("Shift close and login completed")

    def modify_the_order(self):
        self.click_element("(//tr[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0')])[1]")

    def lock_key(self):
        self.click_element('//img[@style="height: 3vh; cursor: pointer; margin-right: 0.7rem;"]')
        self.click_element('//span[text()="Log In"]')

        password = self.data_reader.get_value("password")
        self.fill_text('input[name="password"]', password)
        self.click_element("//button[@id='login']")
        logger.info("Completed login with password only")
        self.page.wait_for_timeout(4000)
        logger.info("POS page loaded successfully")

    def get_total_amount_to_pay(self) -> float:
        total_text = self.get_text(
            '//div[@id="sm-cart-total"]//p[contains(text(), "Total Amount To Pay")]/following-sibling::p')
        total_amount = float(re.findall(r'[\d.]+', total_text)[0])
        logger.info(f"Fetched 'Total Amount To Pay': ₹{total_amount}")
        return total_amount

    def apply_manual_discount_percentage(self):
        # Step 1: Click on Manual Discount
        self.click_element('//span[text()="Manual Discount"]')

        # Step 2: Select "Total Bill Discount %"
        self.click_element('//input[@id="discountName"]')
        self.click_element('//div[text()="Total Bill Discount %"]')
        logger.info("Selected 'Total Bill Discount %'")

        # Step 3: Get the Total Bill before discount
        total_bill_text = self.get_text('//p[contains(text(), "Total Bill")]')
        total_bill_amount = float(re.findall(r'[\d.]+', total_bill_text)[0])
        logger.info(f" Total Bill before discount: ₹{total_bill_amount}")

        # Step 4: Enter Random Discount % (1.00 - 9.99)
        self.page.wait_for_selector('//div[@id="discountValue"]//input[@placeholder="Enter Percentage"]',
                                    state="visible")
        discount_percent = round(random.uniform(1, 9.9), 2)
        self.fill_text('//div[@id="discountValue"]//input[@placeholder="Enter Percentage"]', str(discount_percent))
        logger.info(f"Entered Discount: {discount_percent}%")

        # Step 5: Capture After Discount Amount
        after_discount_text = self.get_text('//p[contains(text(), "After discount")]')
        after_discount_amount = float(re.findall(r'[\d.]+', after_discount_text)[0])
        logger.info(f" Displayed After Discount Amount: ₹{after_discount_amount}")

        # Step 6: Validate Calculation
        expected_discount = round(total_bill_amount * (discount_percent / 100), 2)
        expected_price = round(total_bill_amount - expected_discount, 2)

        if abs(expected_price - after_discount_amount) < 0.01:
            logger.info(" Discount percentage calculation is correct!")
        else:
            logger.error(" Discount validation failed!")
            logger.error(f"Expected After Discount: ₹{expected_price}, but got ₹{after_discount_amount}")
            assert False, "Discount calculation mismatch!"

        # Step 7: Apply Discount
        self.click_element('//span[text()="Apply"]')

        # Optional Step 8: Continue to Payment Flow
        self.click_element('//span[text()="cwsuite"]')
        self.click_element('//input[@id="pinInput"]')
        self.click_element('(//button[text()="1"])[4]')
        self.click_element('(//button[@id="sm-amount-button2"])[3]')
        self.click_element('(//button[text()="1"])[4]')
        self.click_element('(//button[@id="sm-amount-button2"])[3]')
        self.click_element('//span[text()="Approve"]')

        logger.info(f"🎉 Manual Percentage Discount of {discount_percent}% applied and validated successfully.")

    def manual_discount_amount(self):
        # Step 1: Click on Manual Discount
        self.click_element('//span[text()="Manual Discount"]')

        # Step 2: Select "Total Bill Discount Amount"
        self.click_element('//input[@id="discountName"]')
        self.click_element('//div[text()="Total Bill Discount Amount"]')
        logger.info("Selected 'Total Bill Discount Amount'")

        # Step 3: Extract Total Bill before discount
        total_bill_text = self.get_text('//p[contains(text(), "Total Bill")]')
        total_bill_amount = float(re.findall(r'[\d.]+', total_bill_text)[0])
        logger.info(f"Total Bill before discount: ₹{total_bill_amount}")

        # Step 4: Enter Random Discount (including decimals)
        self.page.wait_for_selector('//div[@id="discountValue"]//input[@placeholder="Enter Amount"]', state="visible")
        discount_amount = round(random.uniform(1, 99.99), 2)
        self.fill_text('//div[@id="discountValue"]//input[@placeholder="Enter Amount"]', str(discount_amount))
        logger.info(f"Entered Discount Amount: ₹{discount_amount}")

        # Step 5: Capture After Discount Amount
        after_discount_text = self.get_text('//p[contains(text(), "After discount")]')
        after_discount_amount = float(re.findall(r'[\d.]+', after_discount_text)[0])
        logger.info(f"Displayed After Discount Amount: ₹{after_discount_amount}")

        # Step 6: Validate Calculation
        expected_price = round(total_bill_amount - discount_amount, 2)
        if abs(expected_price - after_discount_amount) < 0.01:
            logger.info(" Discount amount calculation is correct!")
        else:
            logger.error(f" Discount mismatch! Expected ₹{expected_price}, but got ₹{after_discount_amount}")
            raise AssertionError("Manual discount amount validation failed!")

        # Step 7: Apply Discount
        self.click_element('//span[text()="Apply"]')

        # Step 8: Continue to Payment Flow
        self.click_element('//span[text()="cwsuite"]')
        self.click_element('//input[@id="pinInput"]')
        self.click_element('(//button[text()="1"])[4]')
        self.click_element('(//button[@id="sm-amount-button2"])[3]')
        self.click_element('(//button[text()="1"])[4]')
        self.click_element('(//button[@id="sm-amount-button2"])[3]')
        self.click_element('//span[text()="Approve"]')

        logger.info(f"Manual Discount: Applied and validated successfully with amount ₹{discount_amount}")

    def remove_and_validate_discount(self):
        # Get discounted total before removing
        discounted_amount = self.get_total_amount_to_pay()

        # Remove discount
        self.click_element('//span[text()="Manual Discount"]')
        self.click_element("//span[text()='Remove Discount']")
        logger.info("Clicked on Remove Discount")

        # Get total after removing discount
        self.page.wait_for_timeout(2000)  # wait for UI to reflect change
        amount_after_removal = self.get_total_amount_to_pay()

        assert amount_after_removal > discounted_amount, (
            f"Discount removal failed! Expected > ₹{discounted_amount}, got ₹{amount_after_removal}"
        )
        logger.info(f"Discount successfully removed. Amount reset to ₹{amount_after_removal}")

    def process_random_payment(self):
        methods = [
            ("Cash", "//span[text()='Cash']"),
            ("UPI", "//span[text()='UPI']"),
            ("Razor Pay", "//span[text()='Razor Pay']"),
            ("Card", "//span[text()='Card']")
        ]

        self.click_element("//p[text()='Total Amount To Pay']")

        visible = [m for m in methods if self.is_element_visible(m[1], timeout=2)]
        if not visible:
            raise Exception("No payment methods available")

        method, selector = random.choice(visible)
        self.click_element(selector)
        self.click_element("(//button[contains(text(), 'Enter')])[2]")
        logger.info(f"Payment done using {method}")

    def sales_history_for_advance(self):

        invoice_number = self.invoice_no

        self.click_element('//span[text()="Sales History"]')
        self.page.wait_for_timeout(8000)

        search_input = self.page.locator('//input[@placeholder="Search for Customers/Document Number/Contact"]')
        search_input.fill(invoice_number)
        search_input.press("Enter")
        self.page.wait_for_timeout(2000)



    def store_order_amount(self):
        """Store the order amount from the cart (right-side panel)."""
        total_text = self.get_text('//div[@id="sm-cart-total"]')  # e.g., 'Total Amount To Pay\n\n1279.97'
        print(f"[DEBUG] Raw total_text: {total_text}")

        # Extract numeric value using regex
        match = re.search(r"\d+(?:\.\d+)?", total_text)
        if not match:
            raise ValueError(f"❌ Could not find a valid number in total_text: {total_text}")

        total = float(match.group())
        print(f"[DEBUG] Extracted total amount: {total}")

        # Initialize or reuse the list
        if not hasattr(self, 'order_amounts') or self.order_amounts is None:
            self.order_amounts = []

        self.order_amounts.append(total)
        logger.info(f"Stored Order Amount: {total}")
        print(f"✅ Stored Order Amount: {total}")

    def validate_sales_amount(self):
        """Validate order total vs Close Till sales amount."""
        if not hasattr(self, 'order_amounts') or not self.order_amounts:
            raise ValueError("❌ No order amounts stored to validate.")

        expected_sum = round(sum(self.order_amounts), 2)

        # Locate the correct input field (adjust .nth(X) if needed)
        selector = '//input[contains(@class, "transactionAmtInputClose")]'
        locator = self.page.locator(selector).nth(4)  # Example: 5th input field

        locator.scroll_into_view_if_needed()
        sales_amount_str = locator.input_value()

        match = re.search(r"\d+(?:\.\d+)?", sales_amount_str)
        if not match:
            raise ValueError(f"❌ Could not extract a number: {sales_amount_str}")

        sales_amount = float(match.group())

        print(f"🧾 Expected Sum: {expected_sum}")
        print(f"🧾 Sales Amount: {sales_amount}")
        assert expected_sum == round(sales_amount, 2), \
            f"❌ Mismatch: Orders Total = {expected_sum} vs Sales Amount = {sales_amount}"
        print("✅ Sales Amount Validation Passed")

    def log_out_validation(self):
        self.click_element('//img[@style="padding-left: 1rem; height: 2vw;"]')
        self.click_element("//span[text() = 'Logout']")
        self.click_element("//span[text() = 'Next']")
        # self.click_element("//span[text() = 'Next']")
        # self.click_element("//span[text() = 'Close Shift']")
        logger.info(f"log_out: {name}")

    def nan_validation(self):
        self.click_element("//span[text() = 'Next']")
        self.click_element("//span[text() = 'Close Shift']")

    def store_order_id(self):
        """
        Extract the Order ID (e.g., Test 02/1045) and log/check for duplicates.
        """
        order_id_text = self.get_text('//span[contains(text(), "Invoice No:")]')
        print(f"[DEBUG] Raw Order ID Text: {order_id_text}")

        # Corrected regex to capture the full ID
        match = re.search(r'Invoice No:\s*(.+)', order_id_text)
        if not match:
            raise ValueError(f"❌ Could not extract a valid Order ID from: {order_id_text}")

        order_id = match.group(1).strip()
        print(f"[INFO] Extracted Order ID: {order_id}")

        # Duplicate check
        if order_id in self.order_ids:
            print(f"⚠️ Duplicate Order ID Detected: {order_id}")
            logger.warning(f"Duplicate Order ID Detected: {order_id}")
            # Optional: add exit logic or fail the test here
            raise Exception(f"Duplicate Order ID encountered: {order_id}")
        else:
            self.order_ids.append(order_id)
            print(f"✅ Stored Unique Order ID: {order_id}")
            logger.info(f"Stored Order ID: {order_id}")

    # pages/pos_page.py
    # def reopen_in_new_tab(self):
    #     """Copies current URL, opens new tab in same context, closes old tab, and navigates to URL"""
    #     try:
    #         # Get current URL
    #         current_url = self.page.url
    #         logger.info(f"Current URL: {current_url}")
    #
    #         # Create new page in same context
    #         new_page = self.context.new_page()
    #
    #         # Navigate to URL before closing original
    #         new_page.goto(current_url, wait_until="domcontentloaded")
    #
    #         # Close original page
    #         self.page.close()
    #
    #         # Update references
    #         self.page = new_page
    #         self.page.bring_to_front()
    #
    #         logger.info("Successfully transferred to new tab")
    #         return self.page
    #
    #     except Exception as e:
    #         logger.error(f"Failed to transfer to new tab: {str(e)}")
    #         raise

    def coupon_code_without_product(self):
        self.click_element('//span[text()="Coupon Code"]')
        try:

            popup_message = self.page.locator('.ant-message span:has-text("Coupon cant be applied for return items")')
            popup_message.wait_for(state="visible", timeout=5000)  # Wait up to 5 seconds for popup to appear
            expect(popup_message).to_be_visible()
            expect(popup_message).to_have_text("Coupon cant be applied for return items")
            logger.info("Coupon code popup verified successfully: 'Coupon cant be applied for return items'")

            self.page.wait_for_timeout(3000)
            logger.info("Paused for 3 seconds to observe the popup")

            if popup_message.is_visible():
                logger.info("Popup is still visible after 3 seconds")
            else:
                logger.info("Popup auto-dismissed within 3 seconds")

        except TimeoutError:
            logger.error("Coupon code popup did not appear within 5 seconds")
            self.page.screenshot(path="coupon_popup_error.png")
            raise
        except AssertionError as e:
            logger.error(f"Coupon code popup verification failed: {str(e)}")
            self.page.screenshot(path="coupon_popup_error.png")
            raise

    def coupon_code(self):
        try:
            # Extract total amount before coupon
            total_amount_locator = self.page.locator('//div[@id="sm-cart-total"]/p[2]')
            total_amount_locator.wait_for(state="visible", timeout=5000)
            total_amount_text = total_amount_locator.inner_text().strip()
            total_amount = float(total_amount_text)
            print(f"Total Amount To Pay: ₹{total_amount:.2f}")
            logger.info(f"Total Amount To Pay: ₹{total_amount:.2f}")

            # Click Coupon Code element
            self.click_element('//span[text()="Coupon Code"]')
            logger.info("Clicked Coupon Code element")

            # Apply coupon code
            self.click_element('//input[@placeholder="Type Code"]')
            self.page.keyboard.type("1234")
            self.click_element('//span[text()="Apply"]')
            logger.info("Typed 1234 into coupon code input field using keyboard")
            self.click_element('//span[@style="margin: 0.7rem 0px 0.7rem 10px; font-size: 1vw;"]')
            logger.info("clicked cwsuite")
            self.click_element('//input[@placeholder="Enter value"]')
            self.page.keyboard.type("1212")
            logger.info("Typed 1212 into coupon code input field using keyboard")
            self.click_element('//span[text()="Approve"]')
            logger.info("approved")

            # Extract total amount after coupon approval
            total_amount_locator = self.page.locator('//div[@id="sm-cart-total"]/p[2]')
            total_amount_locator.wait_for(state="visible", timeout=5000)
            total_amount_text = total_amount_locator.inner_text().strip()
            total_amount = float(total_amount_text)
            print(f"Total Amount To Pay After Coupon: ₹{total_amount:.2f}")
            logger.info(f"Total Amount To Pay After Coupon: ₹{total_amount:.2f}")

            return total_amount

        except TimeoutError:
            logger.error("Total amount element did not appear within 5 seconds")
            self.page.screenshot(path="total_amount_error.png")
            raise
        except ValueError:
            logger.error(f"Invalid total amount format: {total_amount_text}")
            self.page.screenshot(path="total_amount_error.png")
            raise
        except Exception as e:
            logger.error(f"Error in get_total_amount: {str(e)}")
            self.page.screenshot(path="total_amount_error.png")
            raise

    def coupon_removel(self):
        self.click_element("(//div[contains(@class ,'ant-col ant-col-1')])[1]")
        self.click_element('//span[text()="Coupon Code"]')
        self.click_element('//img[@style="height: 3.5vh; width: 1.5vw; cursor: pointer; position: absolute; right: 0.8vw;"]')

    def custom_box(self, data=None):
        # Open the product selection modal
        self.click_element('//span[@class="anticon anticon-code-sandbox"]')
        self.click_element('//span[text()="Add Products"]')

        # Wait for the product list to load
        product_rows_xpath = "//div[contains(@class, 'ant-row')]//button[contains(@class, 'ant-btn') and .//span[contains(@class, 'anticon-plus')]]/ancestor::div[contains(@class, 'ant-row')]"
        self.page.wait_for_selector(product_rows_xpath, timeout=10000)  # Wait up to 10 seconds for the product list

        # Find all product rows in the current page
        product_rows = self.page.locator(product_rows_xpath)
        total_products = product_rows.count()
        print(f"Found {total_products} products on the current page.")

        if total_products == 0:
            print("No products found in the list.")
            return

        # Determine how many products to select (max 5, or fewer if there aren't enough products)
        num_to_select = min(5, total_products)

        # Randomly select indices for the products
        selected_indices = random.sample(range(total_products), num_to_select)
        print(f"Selected indices: {selected_indices}")

        # Click the '+' button for each selected product
        for index in selected_indices:
            # XPath to locate the '+' button for the specific product row
            plus_button_xpath = f"({product_rows_xpath})[{index + 1}]//button[contains(@class, 'ant-btn') and .//span[contains(@class, 'anticon-plus')]]"
            print(f"Attempting to click '+' button for product at index {index} with XPath: {plus_button_xpath}")

            # Wait for the '+' button to be visible
            self.page.wait_for_selector(plus_button_xpath, timeout=2000)  # Wait up to 5 seconds for the button
            plus_button = self.page.locator(plus_button_xpath).first
            plus_button.click()
            self.page.wait_for_timeout(500)  # Small delay to ensure the UI updates

        # Click OK to close the modal
        self.click_element(
            '//button[@style="background-color: rgb(47, 56, 86); color: rgb(255, 255, 255); width: 8vw; height: 6.5vh; border-radius: 5px; margin-right: 1vw;"]')
        self.click_element('//span[text()="Submit"]')

    def custom_boxes(self):
        self.click_element('//span[@class="anticon anticon-code-sandbox"]')
        # self.click_element('//span[text()="Add Products"]')
        all_buttons_xpath = "//button[@class='ant-btn ant-btn-icon-only']"
        plus_buttons_xpath = "//button[@class='ant-btn ant-btn-icon-only' and .//span[contains(@class, 'anticon-plus')]]"
        self.page.wait_for_selector(all_buttons_xpath, timeout=3000)

        # Find all '+' buttons in the modal
        plus_buttons = self.page.locator(plus_buttons_xpath)
        total_plus_buttons = plus_buttons.count()
        print(f"Found {total_plus_buttons} '+' buttons in the modal.")

        if total_plus_buttons == 0:
            print("No '+' buttons found in the list.")
            return

        # Determine how many '+' buttons to click (max 5, or fewer if there aren't enough buttons)
        num_to_click = min(5, total_plus_buttons)

        # Randomly select indices for the '+' buttons
        selected_indices = random.sample(range(total_plus_buttons), num_to_click)
        print(f"Selected indices for '+' buttons: {selected_indices}")

        # Click each selected '+' button
        for index in selected_indices:
            # Use the exact XPath to locate the specific '+' button by index
            button_xpath = f"({plus_buttons_xpath})[{index + 1}]"
            print(f"Attempting to click '+' button at index {index} with XPath: {button_xpath}")

            # Wait for the button to be visible
            self.page.wait_for_selector(button_xpath, timeout=5000)  # Wait up to 5 seconds for the button
            button = self.page.locator(button_xpath).first
            button.click()
            self.page.wait_for_timeout(500)
            self.click_element('//span[text()="Add Products"]')

            # Wait for the product list to load
            product_rows_xpath = "//div[contains(@class, 'ant-row')]//button[contains(@class, 'ant-btn') and .//span[contains(@class, 'anticon-plus')]]/ancestor::div[contains(@class, 'ant-row')]"
            self.page.wait_for_selector(product_rows_xpath, timeout=10000)  # Wait up to 10 seconds for the product list

            # Find all product rows in the current page
            product_rows = self.page.locator(product_rows_xpath)
            total_products = product_rows.count()
            print(f"Found {total_products} products on the current page.")

            if total_products == 0:
                print("No products found in the list.")
                return

            # Determine how many products to select (max 5, or fewer if there aren't enough products)
            num_to_select = min(5, total_products)

            # Randomly select indices for the products
            selected_indices = random.sample(range(total_products), num_to_select)
            print(f"Selected indices: {selected_indices}")

            # Click the '+' button for each selected product
            for index in selected_indices:
                # XPath to locate the '+' button for the specific product row
                plus_button_xpath = f"({product_rows_xpath})[{index + 1}]//button[contains(@class, 'ant-btn') and .//span[contains(@class, 'anticon-plus')]]"
                print(f"Attempting to click '+' button for product at index {index} with XPath: {plus_button_xpath}")

                # Wait for the '+' button to be visible
                self.page.wait_for_selector(plus_button_xpath, timeout=2000)  # Wait up to 5 seconds for the button
                plus_button = self.page.locator(plus_button_xpath).first
                plus_button.click()
                self.page.wait_for_timeout(500)  # Small delay to ensure the UI updates

            # Click OK to close the modal
            self.click_element(
                '//button[@style="background-color: rgb(47, 56, 86); color: rgb(255, 255, 255); width: 8vw; height: 6.5vh; border-radius: 5px; margin-right: 1vw;"]')
            self.click_element('//span[text()="Submit"]')

    def view_stock(self, tags=None):
        # Wait for the table to load and ensure at least one row exists
        table_rows_xpath = '//tr[contains(@class, "ant-table-row")]'
        try:
            self.page.wait_for_selector(table_rows_xpath, timeout=10000)
            rows = self.page.locator(table_rows_xpath).all()
            if not rows:
                logger.error("No table rows found")
                with open("error_page_content.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                logger.info("Page content saved to 'error_page_content.html'")
                raise AssertionError("No table rows found")
        except Exception as e:
            logger.error(f"Table rows not visible: {str(e)}")
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise

        # Debug: Log all table rows' details
        for i, row in enumerate(rows, 1):
            row_key = row.get_attribute('data-row-key') or 'None'
            row_text = row.inner_text()[:100]  # Limit for brevity
            logger.info(f"Row {i}: data-row-key={row_key}, text={row_text}")

        # Select the first table row
        first_row_xpath = '(//tr[contains(@class, "ant-table-row")])[1]'
        try:
            self.click_element(first_row_xpath)
            logger.info(f"Clicked first table row with XPath: {first_row_xpath}")
        except Exception as e:
            logger.error(f"Failed to click first table row with XPath '{first_row_xpath}': {str(e)}")
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise

        # Extract initial quantity from the second <td>, targeting div with class="tableRow"
        quantity_xpath = f'{first_row_xpath}//td[2]//div[contains(@class, "tableRow")]'
        try:
            quantity_elements = self.page.locator(quantity_xpath).all()
            if len(quantity_elements) != 1:
                logger.error(
                    f"Expected 1 quantity element, found {len(quantity_elements)} for XPath '{quantity_xpath}'")
                for i, elem in enumerate(quantity_elements, 1):
                    logger.info(f"Quantity element {i}: {elem.inner_text()}")
                raise AssertionError(f"XPath '{quantity_xpath}' matched {len(quantity_elements)} elements")
            initial_quantity = float(quantity_elements[0].inner_text().strip())
            logger.info(f"Initial quantity: {initial_quantity}")
        except Exception as e:
            logger.error(f"Failed to extract initial quantity with XPath '{quantity_xpath}': {str(e)}")
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise

        # Extract the initial Total Amount To Pay
        total_amount_xpath = '//div[@id="sm-cart-total"]/p[2]'
        try:
            total_amount = self.page.locator(total_amount_xpath).inner_text().strip()
            self.last_total_amount = float(total_amount)  # Store initial amount
            logger.info(f"Initial Total Amount To Pay: ₹{self.last_total_amount:.2f}")
        except Exception as e:
            logger.error(f"Failed to extract initial Total Amount To Pay with XPath '{total_amount_xpath}': {str(e)}")
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise

        # Calculate unit price
        unit_price = self.last_total_amount / initial_quantity
        logger.info(f"Unit price: ₹{unit_price:.2f} per item")

        # Set random quantity and click Enter
        self.click_element('//div[text()="View Stock"]')
        quantity_input = self.page.locator('//input[@placeholder="Enter Quantity"]')
        quantity_input.click()
        quantity_input.press("Backspace")
        random_quantity = random.randint(1, 10)
        logger.info(f"Random quantity set to: {random_quantity}")
        quantity_input.fill(str(random_quantity))
        self.click_element('//button[text() = "Enter"]')

        # Extract the updated Total Amount To Pay
        try:
            updated_total_amount = self.page.locator(total_amount_xpath).inner_text().strip()
            self.last_updated_total_amount = float(updated_total_amount)  # Store updated amount
            logger.info(f"Updated Total Amount To Pay: ₹{self.last_updated_total_amount:.2f}")
        except Exception as e:
            logger.error(f"Failed to extract updated Total Amount To Pay with XPath '{total_amount_xpath}': {str(e)}")
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise

        # Validate the updated amount
        expected_amount = unit_price * random_quantity
        tolerance = 0.01  # Allow small floating-point errors
        is_valid = abs(self.last_updated_total_amount - expected_amount) <= tolerance
        logger.info(f"Expected amount: ₹{expected_amount:.2f}, Actual amount: ₹{self.last_updated_total_amount:.2f}")
        logger.info(f"Amount validation {'passed' if is_valid else 'failed'}")

        # Specific check for doubling
        if random_quantity == 2 * initial_quantity:
            is_doubled = abs(self.last_updated_total_amount - 2 * self.last_total_amount) <= tolerance
            logger.info(
                f"Doubling validation {'passed' if is_doubled else 'failed'} (Expected: ₹{2 * self.last_total_amount:.2f})")
        else:
            logger.info(
                f"No doubling check (random quantity {random_quantity} != 2 * initial quantity {initial_quantity})")

        # Wait 3 seconds
        self.page.wait_for_timeout(3000)
        logger.info("Waited 3 seconds after reading updated amount")

        # Handle tags
        tags = tags or []  # Empty default
        for tag in tags:
            logger.info(f"Applying tag: {tag}")
            try:
                self.click_element(f'//span[text()="{tag}"]')
            except Exception as e:
                logger.error(f"Failed to apply tag '{tag}' with XPath '//span[text()=\"{tag}\"]': {str(e)}")
                raise

        logger.info("view_stock: completed")

    def over_payment(self):
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        import logging

        logger = logging.getLogger(__name__)

        try:
            # Wait for Total Amount To Pay to be clickable
            self.page.wait_for_selector("//p[text()='Total Amount To Pay']", state="visible", timeout=10000)
            self.click_element("//p[text()='Total Amount To Pay']")
            logger.info("Clicked 'Total Amount To Pay'")

            # Extract product price
            product_price_input = self.page.locator("//input[@id='sm-total-amount-input']")
            self.page.wait_for_selector("//input[@id='sm-total-amount-input']", state="visible", timeout=10000)
            product_price_str = product_price_input.get_attribute("value") or "0.0"
            product_price = float(product_price_str)
            if product_price <= 0.0:
                logger.error("Product price is 0.0 or invalid. Ensure a product with a valid price is added.")
                self.page.screenshot(path="price_error.png")
                logger.info("Screenshot saved as price_error.png")
                raise Exception("Invalid product price")

            logger.info(f"Extracted Product Price: {product_price}")

            # Calculate tendered amount to ensure expected change is 1.00
            tendered_amount = round(product_price + 1.00, 2)
            self.click_element("//span[text()='Cash']")
            logger.info("Selected Cash payment method")
            self.fill_text("//input[@placeholder='Enter Amount']", str(tendered_amount))
            logger.info(
                f"Entered tendered amount: {tendered_amount}, to achieve expected change of 1.00 from product_price: {product_price}")

            # Submit payment
            self.page.wait_for_selector("(//button[contains(text(), 'Enter')])[2]", state="visible", timeout=5000)
            self.click_element("(//button[contains(text(), 'Enter')])[2]")
            logger.info("Clicked 'Enter' to submit payment")

            # Wait for UI to update payment details after submission
            self.page.wait_for_timeout(10000)
            logger.info("Starting payment details extraction after submitting payment")

            # Log DOM for debugging
            dom_content = self.page.content()
            logger.debug(f"DOM content: {dom_content[:1000]}...")

            # Extract payment details
            def get_float_value(xpath, default=0.0):
                try:
                    elements = self.page.locator(xpath).all()
                    texts = [f"{el.inner_text().strip()} (visible: {el.is_visible()})" for el in elements]
                    logger.debug(f"Elements for {xpath}: {texts}")
                    text = self.page.inner_text(xpath, timeout=5000).strip()
                    logger.debug(f"Selected text for {xpath}: {text}")
                    return float(text) if text and text != "" else default
                except (PlaywrightTimeoutError, ValueError) as e:
                    logger.warning(f"Failed to extract value for xpath {xpath}: {e}")
                    return default

            # Extract the change value after payment submission
            change = get_float_value(
                "//div[contains(@class, 'ant-row')]//div[contains(@class, 'ant-col-12') and contains(@style, 'text-align: right')]//p[preceding::p[contains(text(), 'Change')]]",
                default=0.0)

            # Log extracted value
            logger.info(f"Change after payment: {change}")

            # Validation
            is_valid = True
            expected_change = round(tendered_amount - product_price, 2)
            logger.info(f"Expected Change: {expected_change}")

            # Validate that change matches expected_change and is exactly 1.00
            if abs(change - expected_change) > 0.01 or abs(change - 1.00) > 0.01:
                logger.error(
                    f"Change validation failed. Expected Change: {expected_change:.2f}, Actual Change: {change:.2f}, Must be exactly 1.00")
                is_valid = False
            else:
                logger.info("Change validation passed")

            # Take screenshot if validation fails
            if not is_valid:
                logger.error("Change validation failed.")
                self.page.screenshot(path="validation_error.png")
                logger.info("Screenshot saved as validation_error.png")
                raise Exception(
                    f"Change validation failed: Expected Change: {expected_change:.2f}, Actual Change: {change:.2f}, Must be exactly 1.00")
            else:
                logger.info("Change validation passed successfully")

        except Exception as e:
            logger.error(f"Error in over_payment: {e}")
            if self.page and not self.page.is_closed():
                self.page.screenshot(path="error_screenshot.png")
                with open("error_screenshot.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                logger.info("Screenshot saved as error_screenshot.png and HTML saved as error_screenshot.html")
            raise




    def get_total_amount(self):
        try:
            # Extract total amount before coupon
            total_amount_locator = self.page.locator('//div[@id="sm-cart-total"]/p[2]')
            total_amount_locator.wait_for(state="visible", timeout=5000)
            total_amount_text = total_amount_locator.inner_text().strip()
            total_amount = float(total_amount_text)
            print(f"Total Amount To Pay: ₹{total_amount:.2f}")
            logger.info(f"Total Amount To Pay: ₹{total_amount:.2f}")

            # Click Coupon Code element
            self.click_element('//span[text()="Coupon Code"]')
            logger.info("Clicked Coupon Code element")

            # Apply coupon code
            self.click_element('//input[@placeholder="Type Code"]')
            self.page.keyboard.type("1234")
            self.click_element('//span[text()="Apply"]')
            logger.info("Typed 1234 into coupon code input field using keyboard")
            self.click_element('//span[@style="margin: 0.7rem 0px 0.7rem 10px; font-size: 1vw;"]')
            logger.info("clicked cwsuite")
            self.click_element('//input[@placeholder="Enter value"]')
            self.page.keyboard.type("1212")
            logger.info("Typed 1212 into coupon code input field using keyboard")
            self.click_element('//span[text()="Approve"]')
            logger.info("approved")

            # Extract total amount after coupon approval
            total_amount_locator = self.page.locator('//div[@id="sm-cart-total"]/p[2]')
            total_amount_locator.wait_for(state="visible", timeout=5000)
            total_amount_text = total_amount_locator.inner_text().strip()
            total_amount = float(total_amount_text)
            print(f"Total Amount To Pay After Coupon: ₹{total_amount:.2f}")
            logger.info(f"Total Amount To Pay After Coupon: ₹{total_amount:.2f}")

            return total_amount


        except TimeoutError:
            logger.error("Total amount element did not appear within 5 seconds")
            self.page.screenshot(path="total_amount_error.png")
            raise
        except ValueError:
            logger.error(f"Invalid total amount format: {total_amount_text}")
            self.page.screenshot(path="total_amount_error.png")
            raise
        except Exception as e:
            logger.error(f"Error in get_total_amount: {str(e)}")
            self.page.screenshot(path="total_amount_error.png")
            raise

    def cash_management_add_cash(self):
        self.click_element('//span[text()="Cash Management"]')
        self.click_element('//span[text()="Add Cash"]')
        # Generate and store random amount
        random_amount = str(random.randint(1, 200))
        self.last_added_amount = random_amount  # Store for verification
        self.fill_text('//input[@placeholder="e.g, 100"]', random_amount)
        random_text = random.choice(["test", "test case"])
        self.click_element('//input[@placeholder="Type to add a note"]')
        self.fill_text('//input[@placeholder="Type to add a note"]', random_text)
        self.click_element('//span[text()="Done"]')
        self.click_element('//img[@id="sm-cash-management-back"]')
        logger.info(f"addcash: done with amount {random_amount}")


    def Home_logout(self):
        self.click_element('//img[@style="padding-left: 1rem; height: 2vw;"]')
        self.click_element('//span[text()="Logout"]')

    def cash_in(self, tags=None):
        # Define the specific XPath for the Cash In input field
        cash_in_input_xpath = '//div[contains(@class, "ant-form-item-control-input-content")]//p[text()="Cash In"]/..//input[@class="ant-input transactionAmtInput"]'

        # Click the cash-in input element
        self.click_element(cash_in_input_xpath)
        logger.info("Clicked Cash In input field")

        # Ensure the selector resolves to exactly one element
        elements = self.page.locator(cash_in_input_xpath).all()
        if len(elements) != 1:
            logger.error(f"Expected exactly one element for XPath '{cash_in_input_xpath}', found {len(elements)}")
            # Log page content for debugging
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise AssertionError(f"XPath '{cash_in_input_xpath}' matched {len(elements)} elements, expected 1")

        # Extract the displayed amount from the input field
        displayed_amount = self.get_element_attribute(cash_in_input_xpath, 'value')

        # Clean the displayed amount (remove ₹ and whitespace, handle decimals)
        cleaned_amount = displayed_amount.replace('₹', '').strip().split('.')[0]

        # Verify if the displayed amount matches the last added amount
        if self.last_added_amount and cleaned_amount == self.last_added_amount:
            logger.info(f"Cash-in amount validated: {cleaned_amount} matches added amount {self.last_added_amount}")
        else:
            logger.error(
                f"Cash-in amount mismatch! Expected: {self.last_added_amount}, "
                f"Found: {cleaned_amount}"
            )
            raise AssertionError("Cash-in amount mismatch, stopping execution")

        # Handle tags for cash-in (if provided)
        tags = tags or []  # Empty default to skip tags
        for tag in tags:
            logger.info(f"Applying tag: {tag}")
            # Update this XPath based on actual tag UI
            self.click_element(f'//span[text()="{tag}"]')
            logger.info(f"Applied tag: {tag}")

        logger.info("cash_in: completed successfully")

    def cash_management_remove_cash(self):
        self.click_element('//span[text()="Cash Management"]')
        self.click_element('//span[text()="Remove Cash"]')
        # Generate and store random amount
        random_amount = str(random.randint(1, 200))
        self.last_removed_amount = random_amount  # Store for verification
        self.fill_text('//input[@placeholder="e.g, 100"]', random_amount)
        random_text = random.choice(["test", "test case"])
        self.click_element('//input[@placeholder="Type to add a note"]')
        self.fill_text('//input[@placeholder="Type to add a note"]', random_text)
        self.click_element('//span[text()="Done"]')
        self.click_element('//img[@id="sm-cash-management-back"]')
        logger.info(f"removecash: done with amount {random_amount}")

    def cash_remove(self, tags=None):
        # Define the specific XPath for the Cash Out input field
        cash_out_input_xpath = '//div[contains(@class, "ant-form-item-control-input-content")]//p[text()="Cash Out"]/..//input[@class="ant-input transactionAmtInput"]'

        # Click the cash-out input element
        self.click_element(cash_out_input_xpath)
        logger.info("Clicked Cash Out input field")

        # Ensure the selector resolves to exactly one element
        elements = self.page.locator(cash_out_input_xpath).all()
        if len(elements) != 1:
            logger.error(f"Expected exactly one element for XPath '{cash_out_input_xpath}', found {len(elements)}")
            # Log page content for debugging
            with open("error_page_content.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.info("Page content saved to 'error_page_content.html'")
            raise AssertionError(f"XPath '{cash_out_input_xpath}' matched {len(elements)} elements, expected 1")

        # Extract the displayed amount from the input field
        displayed_amount = self.get_element_attribute(cash_out_input_xpath, 'value')

        # Clean the displayed amount (remove ₹ and whitespace, handle decimals)
        cleaned_amount = displayed_amount.replace('₹', '').strip().split('.')[0]

        # Verify if the displayed amount matches the last removed amount
        if self.last_removed_amount and cleaned_amount == self.last_removed_amount:
            logger.info(
                f"Cash-out amount validated: {cleaned_amount} matches removed amount {self.last_removed_amount}")
        else:
            logger.error(
                f"Cash-out amount mismatch! Expected: {self.last_removed_amount}, "
                f"Found: {cleaned_amount}"
            )
            raise AssertionError("Cash-out amount mismatch, stopping execution")

        # Handle tags for cash-out (if provided)
        tags = tags or []  # Empty default to skip tags
        for tag in tags:
            logger.info(f"Applying tag: {tag}")
            # Update this XPath based on actual tag UI
            self.click_element(f'//span[text()="{tag}"]')
            logger.info(f"Applied tag: {tag}")

        logger.info("cash_remove: completed successfully")

    def Custom_mix_name_changing_dynamically(self):
        input_xpath = '//input[@style="width: 300px; border-radius: 5px;"]'

        # Step 1: Click the icon to trigger the input field
        self.click_element('//span[@class="anticon anticon-code-sandbox"]')

        # Step 2: Click the input field (this triggers dynamic name generation)
        self.click_element(input_xpath)

        # Step 3: Wait a bit to let the dynamic value appear
        self.page.wait_for_timeout(500)

        # Step 4: Capture the dynamic name that was generated
        dynamic_name = self.page.locator(input_xpath).input_value()
        print(f"✅ Dynamic name generated by system: {dynamic_name}")

        # Step 5: Generate a fully random name without "Custom_" prefix
        new_custom_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print(f"✏️ Replacing with custom name: {new_custom_name}")

        # Step 6: Replace the input with your custom name
        self.page.locator(input_xpath).fill(new_custom_name)


    def custom_mix_product_search(self):
        self.click_element('//span[text()="Add Products"]')
        self.click_element('//input[@placeholder="Search Item Code / Description"]')


    def custom_mix_add_five_products_by_description(self):
        # Retrieve product descriptions from the JSON test_data using DataReader
        product_descriptions = self.data_reader.get_value("product_descriptions", [])

        # Ensure there are product descriptions to work with
        if not product_descriptions:
            logger.error("No product descriptions found in test_data")
            raise ValueError("No product descriptions found in test_data")

        # Select 5 random product descriptions
        selected_descriptions = random.choices(product_descriptions, k=5)

        # Click on "Add Products" and the search field
        self.click_element('//span[text()="Add Products"]')
        self.click_element('//input[@placeholder="Search Item Code / Description"]')

        # Add each selected product
        for description in selected_descriptions:
            search_input = '//input[@placeholder="Search Item Code / Description"]'
            self.fill_text(search_input, description)
            self.press_enter(search_input)
            time.sleep(1)
            plus_button_xpath = f'//p[contains(text(), "{description}")]/following::button[@class="ant-btn ant-btn-icon-only"][2]'
            self.click_element(plus_button_xpath)
            time.sleep(1)

        # Click "Okay" and "Submit"
        self.click_element('//span[text()="Okay"]')
        self.click_element('//span[text()="Submit"]')

    def custom_mix_qty_change(self):
        self.click_element("(//button[contains(@type,'button')])[3]")
        product_index = random.randint(1, 5)
        self.click_element(f"(//tr[contains(@class, 'ant-table-row-level-1')])[{product_index}]")
        self.page.keyboard.press('+')

    def custom_boxes_delect_product(self):
        self.click_element('//span[@class="anticon anticon-code-sandbox"]')
        delete_buttons = self.page.locator('//img[contains(@src, "delete1.eaf8a42c.svg")]')
        count = delete_buttons.count()

        if count >= 3:
            # Skip index 0
            random_indices = random.sample(range(1, count), 2)
            for index in random_indices:
                delete_buttons.nth(index).click()
        elif count == 2:
            # Only index 1 and 0 exist, skip 0
            delete_buttons.nth(1).click()
        else:
            print("Less than 2 clickable products to delete.")

        self.click_element("//span[text() ='Submit']")



    def reading_values_validation(self):
        try:
            # Wait for the table to load
            self.page.wait_for_selector('tbody.ant-table-tbody', timeout=60000)
            table_body = self.page.locator('tbody.ant-table-tbody')
            print(f"Table body found: {table_body.count()}")

            # Wait for at least one row to appear (this avoids strict mode violation)
            self.page.wait_for_selector('tbody.ant-table-tbody tr[class*="ant-table-row"]', timeout=60000)

            # Get all rows
            row_locator = table_body.locator('tr[class*="ant-table-row"]')
            table_rows = row_locator.all()
            if len(table_rows) == 0:
                raise Exception("No visible data rows found in the table")
            print(f"Found {len(table_rows)} rows")

            # Aggregate values across all rows
            total_qty = 0.0
            total_discount = 0.0
            total_tax = 0.0
            expected_subtotal = 0.0
            total = 0.0

            for i, table_row in enumerate(table_rows, 1):
                print(f"\nProcessing row {i}")
                print(f"Row visible: {table_row.is_visible()}")

                # Skip if the row is not visible
                if not table_row.is_visible():
                    print(f"Row {i} is not visible, skipping...")
                    continue

                # Extract values from the table row
                qty_cell = table_row.locator('td:nth-child(2) .tableRow')
                if qty_cell.count() == 0:
                    raise Exception(f"Quantity cell not found in row {i}")
                qty = float(qty_cell.inner_text())
                print(f"Qty: {qty}")

                discount_cell = table_row.locator('td:nth-child(3) .tableRow')
                if discount_cell.count() == 0:
                    raise Exception(f"Discount cell not found in row {i}")
                discount = float(discount_cell.inner_text())
                print(f"Discount: {discount}")

                tax_cell = table_row.locator('td:nth-child(4) .tableRow')
                if tax_cell.count() == 0:
                    raise Exception(f"Tax cell not found in row {i}")
                tax = float(tax_cell.inner_text())
                print(f"Tax: {tax}")

                price_cell = table_row.locator('td:nth-child(5) .tableRow')
                if price_cell.count() == 0:
                    raise Exception(f"Price cell not found in row {i}")
                price = float(price_cell.inner_text())
                print(f"Price: {price}")

                total_cell = table_row.locator('td:nth-child(6) .tableRow')
                if total_cell.count() == 0:
                    raise Exception(f"Total cell not found in row {i}")
                row_total = float(total_cell.inner_text().replace('₹', '').strip())
                print(f"Total: {row_total}")

                # Aggregate values
                total_qty += qty
                total_discount += discount
                total_tax += tax
                expected_subtotal += price * qty
                total += row_total

            # Extract summary values
            subtotal_row = self.page.locator('div.ant-row:has-text("Subtotal:")')
            subtotal = float(subtotal_row.locator('.ant-col-12:last-child p').inner_text())
            print(f"Subtotal: {subtotal}")

            discount_row = self.page.locator('div.ant-row:has-text("Discount:")')
            summary_discount = float(discount_row.locator('.ant-col-12:last-child p').inner_text())
            print(f"Summary Discount: {summary_discount}")

            tax_row = self.page.locator('div.ant-row:has-text("Tax:")')
            summary_tax = float(tax_row.locator('.ant-col-12:last-child p').inner_text())
            print(f"Summary Tax: {summary_tax}")

            net_value_row = self.page.locator('div.ant-row:has-text("Net Value:")')
            net_value = float(net_value_row.locator('.ant-col-12:last-child p').inner_text())
            print(f"Net Value: {net_value}")

            total_items_qty_row = self.page.locator('div.ant-row:has-text("Total Items / Total Qty:")')
            total_items_qty = total_items_qty_row.locator('.ant-col-12:last-child p').inner_text().split(' / ')
            total_items = int(total_items_qty[0])
            summary_total_qty = float(total_items_qty[1])
            print(f"Total Items / Total Qty: {total_items} / {summary_total_qty}")

            # Validation checks with tolerance
            tolerance = 0.01  # Allow a difference of up to 1 paisa

            # Compare expected subtotal with actual subtotal
            print(f"Expected Subtotal (Sum of Price * Qty): {expected_subtotal}")
            price_subtotal_diff = abs(expected_subtotal - subtotal)
            print(f"Difference between Expected Subtotal and Subtotal: {price_subtotal_diff:.2f}")
            assert price_subtotal_diff <= tolerance, f"Expected Subtotal ({expected_subtotal}) does not match Subtotal ({subtotal}) - Difference: {price_subtotal_diff:.2f}"

            # Compare discount
            discount_diff = abs(total_discount - summary_discount)
            print(f"Difference between Total Discount and Summary Discount: {discount_diff:.2f}")
            assert discount_diff <= tolerance, f"Total Discount ({total_discount}) does not match Summary Discount ({summary_discount}) - Difference: {discount_diff:.2f}"

            # Compare tax
            tax_diff = abs(total_tax - summary_tax)
            print(f"Difference between Total Tax and Summary Tax: {tax_diff:.2f}")
            assert tax_diff <= tolerance, f"Total Tax ({total_tax}) does not match Summary Tax ({summary_tax}) - Difference: {tax_diff:.2f}"

            # Compare total and net value
            total_net_value_diff = abs(total - net_value)
            print(f"Difference between Total and Net Value: {total_net_value_diff:.2f}")
            assert total_net_value_diff <= tolerance, f"Total ({total}) does not match Net Value ({net_value}) - Difference: {total_net_value_diff:.2f}"

            # Compare qty and total qty
            qty_total_qty_diff = abs(total_qty - summary_total_qty)
            print(f"Difference between Total Qty and Summary Total Qty: {qty_total_qty_diff:.2f}")
            assert qty_total_qty_diff <= tolerance, f"Total Qty ({total_qty}) does not match Summary Total Qty ({summary_total_qty}) - Difference: {qty_total_qty_diff:.2f}"

            # Validate total items
            assert total_items == len(
                table_rows), f"Total Items ({total_items}) does not match number of rows ({len(table_rows)})"

            # Validate total calculation
            calculated_total = expected_subtotal + total_tax - total_discount
            calculated_total_diff = abs(calculated_total - total)
            print(f"Difference between Calculated Total and Total: {calculated_total_diff:.2f}")
            assert calculated_total_diff <= tolerance, f"Calculated Total ({calculated_total}) does not match Total ({total}) - Difference: {calculated_total_diff:.2f}"

            print("All validations passed!")
        except Exception as e:
            print(f"Validation failed: {str(e)}")
            self.page.screenshot(path="error_screenshot.png")
            raise


    def sand_box(self):
        self.click_element('//span[@aria-label="code-sandbox"]')




####################################----OFC----FUNCIONS-------################################################

    #Validation of Discount 20% calculating

    def ofc_validation_discount(self):
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        import logging
        import re

        logger = logging.getLogger(__name__)

        try:
            # Wait for invoice table rows to be visible
            self.page.wait_for_selector("//tr[contains(@class, 'ant-table-row')]", state="visible", timeout=10000)

            # Extract all rows
            rows = self.page.locator("//tr[contains(@class, 'ant-table-row')]").all()
            if not rows:
                logger.error("No products found in the invoice table")
                raise Exception("No products found in the invoice table")

            logger.info(f"Found {len(rows)} products in the invoice table")

            # Extract and validate each product
            def get_float_value(locator, default=0.0):
                try:
                    text = locator.inner_text(timeout=5000).strip()
                    # Remove all non-numeric characters except the first dot
                    cleaned_text = re.sub(r'[^\d.]', '', text)
                    cleaned_text = re.sub(r'\.+', '.', cleaned_text)
                    cleaned_text = cleaned_text.rstrip('.')
                    return float(cleaned_text) if cleaned_text and cleaned_text != '.' else default
                except (PlaywrightTimeoutError, ValueError) as e:
                    logger.warning(f"Failed to extract value: {e}")
                    return default

            is_valid = True
            for i, row in enumerate(rows, 1):
                quantity = get_float_value(row.locator("td:nth-child(2)"), default=1.0)
                price = get_float_value(row.locator("td:nth-child(5)"), default=0.0)
                discount = get_float_value(row.locator("td:nth-child(3)"), default=0.0)
                total = get_float_value(row.locator("td:nth-child(6)"), default=0.0)

                # Calculate expected discount and total for 20% discount
                total_price = price * quantity
                expected_discount = round(total_price * 0.20, 2)
                expected_total = round(total_price - expected_discount, 2)

                # Log all values in the requested format
                logger.info(f"Product {i}: Quantity: {quantity}, Price: {price}, "
                            f"Expected Discount: {expected_discount}, Discount: {discount}, "
                            f"Expected Total: {expected_total}, Total: {total}")

                # Validate discount and total
                if abs(discount - expected_discount) > 0.01 or abs(total - expected_total) > 0.01:
                    logger.error(f"Product {i} - Discount validation failed. "
                                 f"Expected Discount: {expected_discount:.2f}, Actual Discount: {discount:.2f}, "
                                 f"Expected Total: {expected_total:.2f}, Actual Total: {total:.2f}")
                    is_valid = False
                else:
                    logger.info(f"Product {i} - Discount validation passed")

            # Take screenshot if validation fails
            if not is_valid:
                self.page.screenshot(path="discount_validation_error.png")
                logger.info("Screenshot saved as discount_validation_error.png")
                raise Exception("Discount validation failed for one or more products")
            else:
                logger.info("Discount validation passed successfully for all products")

        except Exception as e:
            logger.error(f"Error in ofc_validation_discount: {e}")
            if self.page and not self.page.is_closed():
                self.page.screenshot(path="error_screenshot.png")
                logger.info("Screenshot saved as error_screenshot.png")
            raise




    ##############cash Payment OFC#######################

    def cash_payment_full_dynamic_round_off(self):
        total_amount_text = self.page.inner_text("//p[text()='Total Amount To Pay']/following-sibling::p")
        total_amount = float(total_amount_text.replace("₹", "").strip())
        # Store original amount
        self.cash_order_totals.append(total_amount)
        # Print in console
        print(f"[Order Paid] Total Amount To Pay (Before Round Off): ₹{total_amount}")
        # Round and pay
        rounded_amount = math.ceil(total_amount)
        self.click_element("//p[text()='Total Amount To Pay']")
        self.click_element("//span[text()='Cash']")
        self.fill_text("//input[@placeholder='Enter Amount']", str(rounded_amount))
        self.click_element("(//button[contains(text(), 'Enter')])[2]")

    def validate_cash_sale_amount_and_continue(self):
        total_paid = round(sum(self.cash_order_totals), 2)
        print(f"🔄 Total Sum of All Orders Paid: ₹{total_paid}")

        # Correct XPath for readonly input
        raw_value = self.page.get_attribute(
            "//p[text()='Cash Sale Amount']/following::input[@class='ant-input transactionAmtInput'][1]",
            "value"
        )
        print(f"🧾 Raw Field Value: {raw_value}")

        # ✅ Extract float from mixed currency string
        import re
        match = re.search(r"(\d+\.\d+)", raw_value)
        if match:
            clean_value = match.group(1)
            sale_amount = float(clean_value)
        else:
            print(f"❌ Couldn't extract float from: '{raw_value}'")
            self.page.context.close()
            return

        if round(sale_amount, 2) == total_paid:
            print("✅ Match! Clicking Next.")
        else:
            print(f"❌ Mismatch: Expected ₹{total_paid}, got ₹{sale_amount}")
            self.page.context.close()

    def ofc_purpose_cash_sale_validation(self):
        self.click_element("//span[text() = 'Next']")

    def click_random_product(self):
        # Locate all product rows
        product_rows = self.page.locator(
            "//tr[contains(@class, 'ant-table-row') and contains(@class, 'ant-table-row-level-0')]")

        # Count how many rows are present
        count = product_rows.count()
        print(f"Found {count} products")

        if count == 0:
            print("❌ No products found to click")
            return

        # Choose a random row index
        random_index = random.randint(0, count - 1)
        print(f"Clicking on product row index: {random_index + 1}")

        # Click on the randomly selected row
        product_rows.nth(random_index).click()













