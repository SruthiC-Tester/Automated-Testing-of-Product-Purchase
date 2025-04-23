import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSpreeCommerce:

    @pytest.fixture(scope="function")
    def setup_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://demo.spreecommerce.org/")
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        yield
        self.driver.quit()

    def test_spreecommerce_site_login(self, setup_browser):
        assert "Spree Commerce DEMO" in self.driver.title
        self.driver.quit()

    def test_invalid_spreecommerce_site_login(self, setup_browser):
        assert "Spree Commerce DEMO 123" in self.driver.title
        self.driver.quit()

    def test_fashion_page_loading(self, setup_browser):
        fashion_menu = self.driver.find_element(By.XPATH, '//*[@id="block-6468"]/a/span')
        actions = ActionChains(self.driver)
        actions.move_to_element(fashion_menu).perform()

        men_section = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="block-6468"]/div/div/div/div[2]/h6'))
        )

        assert men_section.is_displayed()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.quit()

    def test_TShirt_page_loading(self, setup_browser):
        fashion_menu = self.driver.find_element(By.XPATH, '//*[@id="block-6468"]/a/span')
        actions = ActionChains(self.driver)
        actions.move_to_element(fashion_menu).perform()

        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="block-6468"]/div/div/div/div[2]/h6'))
        )

        tshirt_link = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="block-6468"]/div/div/div/div[2]/div[1]/a/span')
        ))
        tshirt_link.click()

        WebDriverWait(self.driver, 40).until(EC.title_contains("T-Shirts"))
        assert "t-shirts" in self.driver.title.lower()

        self.wait.until(EC.presence_of_element_located((By.ID, "products_list")))
        products = self.driver.find_elements(By.CLASS_NAME, 'product-card-inner')

        self.wait = WebDriverWait(self.driver, 20)

        extracted_data = []
        for product in products:
            try:
                name = product.find_element(By.CLASS_NAME, 'product-card-title').text
            except:
                name = "name not found"

            try:
                price = product.find_element(By.CLASS_NAME, 'product-card-price').text
            except:
                price = "Price not available"

            extracted_data.append({"name": name, "price": price})

        print("Extracted Products:\n")
        for item in extracted_data:
            print(f"Name: {item['name']}\nPrice: {item['price']}\n")

        expected_products = [
            "Ripped T-Shirt",
            "Pink Polo Shirt",
            "Red Polo Shirt",
            "Blue Polo Shirt",
            "Spree T-Shirt"
        ]

        extracted_names = [item['name'] for item in extracted_data]
        for expected in expected_products:
            if expected in extracted_names:
                print(f"✔️ Product found: {expected}")
            else:
                print(f"❌ Product missing: {expected}")
        self.driver.quit()