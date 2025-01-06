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
        return page
        
        
# if __name__ == "__main__":
#     login_to_linkedin("swapnilsonker04@gmail.com", "Swapnil@04")        
        