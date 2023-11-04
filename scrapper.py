from playwright.sync_api import Playwright, sync_playwright, expect
import re
from bs4 import BeautifulSoup

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    url = "https://rede-expressos.pt/pt"


    page = context.new_page()
    page.goto(url)
    page.get_by_label("Selecione Origem").click()
    page.get_by_role("option", name="Lisboa (Sete Rios)").click()
    page.get_by_label("Selecione Destino").click()
    page.get_by_role("option", name="Braga", exact=True).click()
    page.get_by_placeholder("Choose Date").click()
    page.get_by_label("25-11-2023").click()
    page.locator("div").filter(has_text=re.compile(r"^Passageiros1x Adulto \(30 a 64\)Pesquisar$")).locator("svg").click()
    page.locator("div:nth-child(2) > div:nth-child(2) > .QuantityPicker--quantityPicker--0de2c > svg:nth-child(3)").click()
    page.locator(".quantityModifier").first.click()
    page.locator(".MuiFormControl-root > .MuiInputBase-root > .MuiSvgIcon-root").click()
    page.get_by_role("button", name="Pesquisar").click()
    page.wait_for_timeout(5000)
    
    # HTML from page
    page_content = page.inner_html('#outgoing-trip-results-section')

    # Open file to write content
    results_file = open('ren_content.html', 'w')
    
    # Pass through BeautiflSoup to process  
    soup = BeautifulSoup(page_content)

    # Write content to file and close it afterwards
    results_file.write(soup.prettify())
    results_file.close()

    results = soup.find_all(class_='MuiPaper-root MuiCard-root jss1179 MuiPaper-elevation1 MuiPaper-rounded')
    print(results)

    # ---------------------
    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)

