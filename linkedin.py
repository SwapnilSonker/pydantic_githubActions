from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler 
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import threading
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()

Email = os.getenv("Linkedin_mail")
Password = os.getenv("Linkedin_password")

email_password = os.getenv("Email_password")

def send_notification(subject, message):
    try:
        sender_email = "swapnilsonker04@gmail.com"
        sender_password = email_password
        receiver_email = "swapnilsonker04@gmail.com"
        
        email = MIMEMultipart()
        email['From'] = sender_email
        email['To'] = receiver_email
        email['Subject'] = subject
        email.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, email.as_string())
        server.quit()
        
        print(f"Notification sent: {subject}")
    except Exception as e:
        print(f"Failed to send notification :{e}")    
    
    
    

def login_to_linkedin(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to LinkedIn login page
        page.goto("https://www.linkedin.com/login")
        print("LinkedIn opened successfully")
        
        # Log in to LinkedIn
        page.fill("input#username", username)
        page.fill("input#password", password)
        page.click("button[type='submit']")
        
        page.wait_for_timeout(5000)
        page.wait_for_url("https://www.linkedin.com/feed/")
        print("Logged in successfully!!")
        send_notification("Job Started", "The LinkedIn bot job has started running, logged in successfully.")
        
        # Search for "YC"
        search_input = page.locator('.search-global-typeahead__input')
        search_input.wait_for(state='visible', timeout=10000)
        search_input.click()
        # print("Search field clicked successfully")
        search_input.fill("YC")
        search_input.press('Enter')
        page.wait_for_timeout(10000)
        
        # Filter search results by "People"
        page.get_by_role("button", name="People").click()
        # print("Filtered by 'People'")
        request_connect = 0
        max_requests = 15
        while request_connect <= max_requests:
            
            
            scroll_attempts = 0

            # Start connecting with people
            while scroll_attempts < 3:  # Stop after 3 attempts without finding new results
                connect_buttons = page.locator('//button//span[text()="Connect"]')
                count_connect = connect_buttons.count()
                
                if count_connect == 0:
                    print("No 'Connect' buttons found. Scrolling down...")
                    page.mouse.wheel(0, 1000)
                    sleep(2)
                    scroll_attempts += 1
                    continue
                
                # scroll_attempts = 0  # Reset scroll attempts if buttons are found
                print(f"Found {count_connect} 'Connect' buttons on the page.")
                
                for i in range(count_connect):
                    try:
                        # Click on the "Connect" button
                        connect_buttons.nth(i).click()
                        # print(f"Clicked 'Connect' button {i + 1}")
                        page.wait_for_timeout(5000)
                        
                        # Check for the "Send" button and click if visible
                        send_button = page.locator('//button//span[text()="Send"]')
                        if send_button.is_visible():
                            send_button.click()
                            request_connect += 1
                            # print("Clicked 'Send' button.")
                        else:
                            print("No 'Send' button found.")
                    except Exception as e:
                        print(f"Error clicking button {i + 1}: {e}")
                
                # Scroll down to load more buttons
                # print("Scrolling down to load more connections...")
                page.mouse.wheel(0, 1000)
                sleep(5)
            next_button = page.locator('//button//span[text()="Next"]')   
            if next_button.is_visible():
                next_button.click()
                page.wait_for_timeout(5000)
            else:
                print("No next button is found.")
                break
            
        browser.close()        

def job_listener(event):
    if event.exception:
        print(f"job failed: {event.job_id}")
        send_notification(
        "Job Failed", 
        f"The LinkedIn bot job failed with Job ID: {event.job_id}"
        )
    else:
        print(f"job completed successfully: {event.job_id}")
        send_notification(
        "Job Completed", 
        f"The LinkedIn bot job finished successfully with job id : {event.job_id}"
        )
    
    print("scheduler exited from function")    
    threading.Thread(target=scheduler.shutdown).start()
            
                

if __name__ == "__main__":
    
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(lambda:login_to_linkedin(Email, Password) , 'cron', hour=13, minute=38)
    
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    try:
        print("Scheduler started")
        scheduler.start()
        while scheduler.get_jobs():
            sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("scheduler exited from main")
        scheduler.shutdown()
    
