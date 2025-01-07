import re
from playwright.sync_api import sync_playwright 

def login_to_linkedin(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.linkedin.com/login")
        print("Linkedin opened successfully")
        
        page.fill("input#username", username)
        page.fill("input#password" , password)
        page.click("button[type='submit']")
        
        page.wait_for_timeout(5000)
        
        page.wait_for_url("https://www.linkedin.com/feed/")
        
        print("Logged in successfully!!")
        
        search_input = page.locator('.search-global-typeahead__input')

# Wait for the search input field to be visible and interactable
        search_input.wait_for(state='visible', timeout=10000)

        # Click on the search input field
        search_input.click()

        print("Search field clicked successfully")
        # search = page.locator('input[aria_label="Search"]')
        # search.wait_for(state="visible", timeout=15000)
        search_input.fill("YC 23")
        search_input.press('Enter')
        print("search enteres successfully")
        # page.wait_for_timeout(10000)
        return page



            
        
if __name__ == "__main__":
    login_to_linkedin("swapnilsonker04@gmail.com", "Swapnil@04")        
        