from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Setup WebDriver
def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment if you want headless mode
    path_to_chromedriver = "C:\\Users\\slim\\OneDrive\\Desktop\\win_64\\chromedriver-win64\\chromedriver.exe"
    service = Service(path_to_chromedriver)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_partner_names(driver):
    driver.get("https://www.cve.org/PartnerInformation/ListofPartners")
    wait = WebDriverWait(driver, 10)

    # Wait for dropdown and select "All"
    select_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[aria-label="select how many partners to show"]'))
    )
    select = Select(select_element)
    select.select_by_visible_text("All")
    time.sleep(5)  # Wait for full load after selection

    # Get partner rows
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr[data-v-d791665f]')
    partner_names = []
    for row in rows:
        try:
            link = row.find_element(By.XPATH, './/a')
            partner_names.append(link.text)
        except:
            continue
    return partner_names


def search_partner(driver, partner_name):
    wait = WebDriverWait(driver, 10)

    # Close popup if present
    try:
        close_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".svg-inline--fa.fa-xmark")))
        close_icon.click()
        print("Close icon clicked.")
        time.sleep(1)
    except:
        print("Close button not visible. Proceeding...")

    print("Searching partner:", partner_name)

    # Search box interaction
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Enter search terms"]')))
    search_box.clear()
    first_word = partner_name.split(' ')[0]
    search_box.send_keys(first_word)
    search_box.send_keys(Keys.RETURN)

    # Wait for results table
    tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cve-main-page-content > div.table-container > table > tbody")))

    # Extract and print rows
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    headers = ["Partner", "Scope", "Program Role", "Organization Type", "Country*"]
    print("\t".join(headers))  # Print headers separated by tabs
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        cell_texts = [cell.text for cell in cells]
        print("\t".join(cell_texts))


if __name__ == "__main__":
    driver = setup_driver()
    try:
        partners = get_partner_names(driver)
        for partner in partners:
            search_partner(driver, partner)
    finally:
        driver.quit()
