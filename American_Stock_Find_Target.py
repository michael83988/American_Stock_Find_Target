from playwright.sync_api import sync_playwright
import numpy as np


def get_historic_price(abbr, playwright, avg_type):
    # Get specific company's historical price then calculate its 20MA price (price per month)
    url = "https://finance.yahoo.com/"

    chromium = playwright.chromium # or "firefox" or "webkit".    
    browser = chromium.launch(headless = False)
    context = browser.new_context(
        # viewport={'width': 1600, 'height':1200}
        )  # Allowed to create multiple pages with the same set of custom header
    page = context.new_page()  # Create a new page
    page.goto(url, timeout = 120000, wait_until = "domcontentloaded")
    print("'Yahoo finance' requested completely!")


    # 找到輸入公司簡稱的input
    page.get_by_placeholder("Quote Lookup").type(abbr, delay = 2000 + np.random.rand() * 2000)
    # page.get_by_placeholder("Quote Lookup").focus()
    smart_hint_selector = "css=[data-id=search-assist-input-sugglst]"
    page.wait_for_selector(smart_hint_selector, state = "attached", timeout = 30000)
    page.keyboard.press("Enter", delay = np.random.rand() * 1000 + 1000)   

    
    # 取得跳轉該公司頁面後的公司名稱
    com_name_selector = "#quote-header-info > div.Mt\(15px\).D\(f\).Pos\(r\) > div.D\(ib\).Mt\(-5px\).Maw\(38\%\)--tab768.Maw\(38\%\).Mend\(10px\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1"
    company_name = page.wait_for_selector(com_name_selector, state = "attached", timeout = 30000)  



    print("Get targeted company completely!")  
    print(company_name.inner_text())       


    # 點hisotorical data
    # type_selector = "#quote-nav > ul > li.IbBox.Fw\(500\).fin-tab-item.H\(44px\).desktop_Bgc\(\$hoverBgColor\)\:h.desktop-lite_Bgc\(\$hoverBgColor\)\:h.selected > a > span"           
    #quote-nav > ul > li.IbBox.Fw\(500\).fin-tab-item.H\(44px\).desktop_Bgc\(\$hoverBgColor\)\:h.desktop-lite_Bgc\(\$hoverBgColor\)\:h.selected > a > span
    # page.wait_for_selector(type_selector, state = "attached", timeout = 30000).click(timeout = 5000, delay = np.random.rand() * 1000)
    page.get_by_text("Historical Data").hover(timeout = 30000)
    page.get_by_text("Historical Data").click(timeout = 30000, delay = np.random.rand() * 10000)
    print("點歷史資料")

    # 點Frequency: Monthly
    # page.wait_for_selector(smart_hint_selector, state = "attached", timeout = 30000)
    page.get_by_text("Daily").click(timeout = 30000, delay = np.random.rand() * 3000)
    menu = page.locator("data-test=historicalFrequency-menu")
    # page.locator("css=[data-value=1mo]").click(timeout = 5000, delay = np.random.rand() * 1000)
    menu.get_by_text("Monthly").click(timeout = 30000, delay = np.random.rand() * 3000)
    print("選擇月為單位")
    # range_menu = page.locator("id=dropdown-menu").click(timeout = 30000, delay = np.random.rand() * 1000)
    # range_menu = page.locator("[data-test=dropdown]").click(timeout = 30000, delay = np.random.rand() * 3000)
    range_menu = page.get_by_text("Aug 28, 2022 - Aug 28, 2023").click(timeout = 30000, delay = np.random.rand() * 3000)
    print(range_menu.inner_html())
    print("找到時間範圍選擇")
    range_menu.get_by_text("5Y").click(timeout = 30000, delay = np.random.rand() * 3000)
    # range_menu.get_by_text("Done").click(timeout = 30000, delay = np.random.rand() * 1000)

    page.get_by_text("Apply").click(timeout = 30000, delay = np.random.rand() * 1000)
    his_table = page.locator("data-test=historical-prices")
    print(his_table.inner_text())
    # page.screenshot(path = "screenshot1.png")



    print("OK")

    # current_url = page.url
    # print(menu.inner_html())








if __name__ == "__main__":
    with sync_playwright() as playwright:
        get_historic_price("AAPL", playwright, "20MA")
