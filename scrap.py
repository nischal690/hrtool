import datetime
import playwright.sync_api as sync_playwright
import traceback  # Import traceback explicitly

desired_download_path = r'C:\Users\Administrator\Downloads'



# Start Playwright in a context manager to ensure it closes correctly
def perform_scraping_task():
    try:
        with sync_playwright.sync_playwright() as playwright:
            browser = playwright.chromium.launch_persistent_context(
                  # Note: Using slow_mo for demonstration; adjust as needed
                channel='chrome',
                downloads_path=desired_download_path,  # Use the Chrome browser
                user_data_dir=r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data',  # Ensure this path is correct
                headless=False  # Run in headful mode
            )
            page = browser.new_page()
            page.goto("https://www.naukri.com/recruit/login")

            # Login sequence starts here
            try:
                page.click("#loginRegTab")
                email_id = input("Please enter your registered email ID: ")
                page.fill('input[name="username"]', email_id)
                password = input("Please enter your password: ")
                page.fill('input[name="password"]', password)
                page.click("button.submit_button_1.rcom-btn-primary.rcom-btn-regular")
                page.wait_for_selector('input[name="mobileOtp"], .HjuAK', state='attached', timeout=10000)

                otp_field = page.query_selector('input[name="mobileOtp"]')
                if otp_field:
                    otp = input("Please enter the OTP received on mobile / email: ")
                    page.fill('input[name="mobileOtp"]', otp)
                    page.click("button.otp-verify-btn.rcom-btn-primary.rcom-btn-regular")

                page.wait_for_selector('.HjuAK', state='visible')
                print("Hovering over 'Resdex' div...")
                page.hover("div.xzaIN:has-text('Resdex')")
                print("Successfully hovered over 'Resdex' div.")
                page.click("a.I3sTS[href*='//resdex.naukri.com/v3']")

                if page.query_selector("div.pTB20:has-text('Someone is already logged into Resdex with this username.')"):
                    print("Detected another session is active. Attempting to reset subuser login.")
                    page.click("a[href*='/v2/ResetLogin/displayResetLogin']")
                    page.wait_for_selector("input#resetLoginRadioBtn", state='attached', timeout=10000)
                    page.click("input#resetLoginRadioBtn")
                page.wait_for_selector("h1.heading-l:has-text('Search candidates')", timeout=10000)
                print("Successfully reset subuser login and navigated to the 'Search candidates' page.")

                # Keywords input and search
                while True:
                    keyword = input("Enter a keyword like skills, designation, and company (type 'exit' to finish): ")
                    if keyword.lower() == 'exit':
                        break
                    page.fill("input[name='ezKeywordsAny']", keyword)
                    page.wait_for_selector("ul.layer-wrap li.tuple-wrap", state="visible")
                    page.click("ul.layer-wrap li.tuple-wrap:first-child")
                    print("Initiating search...")

                page.click("#adv-search-btn")
                profiles_found_selector = "h1.top-band-header.ellipsis"
                page.wait_for_selector(profiles_found_selector, state='visible', timeout=30000)
                profiles_text = page.text_content(profiles_found_selector)
                number_of_profiles = profiles_text.split(' ')[0].replace(',', '')
                print(f"Number of profiles found: {number_of_profiles}")

                # Process each candidate
                candidate_links = page.query_selector_all('a.candidate-name')
                for index, link in enumerate(candidate_links):
                    with page.context.expect_page() as new_page_info:
                        link.click()
                    new_page = new_page_info.value
                    new_page.wait_for_selector('span.hlite-inherit', state='attached')
                    button_locator = page.locator(
        'button.\_7A8ek.flex-row.flex-aic.naukri-btn-secondary.naukri-btn-small[type="button"][label="Small"] >> span:has-text("View phone number")'
    )
                    button_locator.click() 
                    new_page.evaluate("""async () => {
        const scrollStep = window.innerHeight / 10;  // Adjust the step size as needed
        const scrollInterval = 100;  // Adjust the interval as needed
        for (let i = 0; i < document.body.scrollHeight; i += scrollStep) {
            window.scrollBy(0, scrollStep);
            await new Promise(resolve => setTimeout(resolve, scrollInterval));
        }
    }""")
                    new_page.evaluate("""() => {
        const hideElements = (selectors) => {
            selectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    element.style.display = 'none';
                });
            });
        };
        hideElements([
            '.right-section.sticky',
            '.cv-prev-header',
            '.actionbar-wrapper'
            '.naukri-tooltip-wrapper'
        ]);
    }""")
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    pdf_filename = f'candidate_profile_{index}_{timestamp}.pdf'
                    pdf_path = f'C:\\Users\\Administrator\\Downloads\\{pdf_filename}'
                    new_page.pdf(path=pdf_path, format='A4', printBackground=True, margin={'top': '0px', 'bottom': '0px', 'left': '0px', 'right': '0px'})
                    new_page.wait_for_timeout(2000)
                    with new_page.expect_download() as download_info:
                        download_button_selector = 'button[aria-label="Download Resume"]'
                        new_page.locator(download_button_selector).wait_for(state='visible')

                        new_page.evaluate(f"""
        const button = document.querySelector('{download_button_selector}');
        button.scrollIntoView({{
            behavior: 'smooth',
            block: 'center',
            inline: 'center'
        }});
        window.scrollBy(0, -50);  // Offset to ensure clickability
    """)

                        new_page.wait_for_timeout(1000) 
                        new_page.click(download_button_selector)
                    download = download_info.value
                    download_path = download.path()
                    print(f"Resume downloaded to: {download_path}")
                    new_page.close()

            except Exception as e:
                print("An error occurred:")
                traceback.print_exc()
            finally:
                browser.close()
                print("Browser closed.")
    except:
        pass
perform_scraping_task() 

   
