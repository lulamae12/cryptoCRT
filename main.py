import random,requests,time
import numpy as np
import plotext as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from rich.console import Console
from rich.layout import Layout
import rich
from rich.progress import Progress, SpinnerColumn, Spinner, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn,TransferSpeedColumn
from rich.panel import Panel
from rich.table import Table


#selenium options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("chromedriver.exe", options=options)  

def getCRYPTOFact():
    facts = open('cryptoFacts.txt', 'r', encoding="utf8")
    Lines = facts.readlines()
    randomFact = random.randrange(0,len(Lines))
    return Lines[randomFact]


def getCRYPTOPrice(name): 
    # Get the current price of Bitcoin in USD using the coindesk.com API with Python and the Requests HTTP library
    URL = 'https://www.coindesk.com/price/' + name
    driver.get(URL)
    page = driver.page_source

    
    #format output
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find(id='export-chart-element')
    price = results.find('div', class_='price-large')
    price = str(price).replace('<div class="price-large"><span class="symbol">$</span>','')
    price = str(price).replace('</div>','')
    price = str(price).replace(',','')


    
    #close selnenium
    
    
    return float(price)


def graphBTC():
    chageStr = ""
    oldPrice = 1
    priceArray = []
    count = 0
    while count < 10: 
        for i in range(10):
            currentPrice = getCRYPTOPrice("bitcoin")
            change = currentPrice - oldPrice
            change = (change/oldPrice)*1000

            if change > 0:
                changeStr = " ▲ ( +"
            elif change < 0:
                changeStr = " ▼ ( "
            else:
                changeStr = " - (  "



            oldPrice = currentPrice
            priceArray.append(float(change))
            plt.clp()
            plt.clt()
            plt.plot(priceArray,line_marker = "─",point_marker = "■",label = "BTC %")

            #place attrs below

            
            
            plt.axes(False,False)

            plt.ylim(-3,3)
            plt.xlim(0,10)
            plt.title(str("CURRENT BTC PRICE [USD] : $" + str(currentPrice) + changeStr + "{:.2f}".format(change) + " % ) " ))
            plt.ylabel("% Change")
            
            


            plt.nocolor()
            plt.show()
        
        count = count + 1
        priceArray.clear()
        priceArray.append(0)

#amount ran is counter X 10
def getBTC(counter):
    for i in range(counter):
        graphBTC()

def graphETH():
    chageStr = ""
    oldPrice = 1
    priceArray = []
    count = 0
    while count < 10: 
        for i in range(10):
            currentPrice = getCRYPTOPrice("ethereum")
            change = currentPrice - oldPrice
            change = (change/oldPrice)*1000

            if change > 0:
                changeStr = " ▲ ( +"
            elif change < 0:
                changeStr = " ▼ ( "
            else:
                changeStr = " - (  "



            oldPrice = currentPrice
            priceArray.append(float(change))
            plt.clp()
            plt.clt()
            plt.plot(priceArray,line_marker = "─",point_marker = "■",label = "ETH %")

            #place attrs below
            plt.axes(False,False)
            plt.ylim(-3,3)
            plt.xlim(0,10)
            plt.title(str("CURRENT ETH PRICE [USD] : $" + str(currentPrice) + changeStr + "{:.2f}".format(change) + " % ) " ))
            plt.ylabel("% Change")
            plt.nocolor()
            plt.show()
        count = count + 1
        priceArray.clear()
        priceArray.append(0)

#amount ran is counter X 10
def getETH(counter):
    for i in range(counter):
        graphETH()

def scrapeRawData(currency):

    
    # Get the current price of Bitcoin in USD using the coindesk.com API with Python and the Requests HTTP library
    URL = 'https://www.coindesk.com/price/' + currency
    page = requests.get(URL)

    #format output
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='export-chart-element')
    

    #get and format data
    #price change data
    priceChange = results.find('div', class_='percent-change-medium')
    priceChangeUpOrDown = str(priceChange).replace('<div class="percent-change-medium"><svg class="chevron-arrow','')
    priceChangeUpOrDown = priceChangeUpOrDown.split('"')[0]
    
    priceChange = str(priceChange).replace('<div class="percent-change-medium"><svg class="chevron-arrow price-up" height="11" viewbox="0 0 22 11" width="22"><path d="M0.3,11L11,1l10.7,10"></path></svg><span class="price-color up"><span class="percent-value-text">','')
    priceChange = str(priceChange).replace('</span><span class="symbol">%</span></span></div>','')
    
    #get market cap
    marketCap = results.find_all('div', class_='data-definition')[2]
    marketCap = str(marketCap).replace('<div class="data-definition"><div class="price-medium">$','')
    marketCap = str(marketCap).replace('</div></div>','')
    
    #get market vol
    marketVol = results.find_all('div', class_='data-definition')[3]
    marketVol = str(marketVol).replace('<div class="data-definition"><div class="price-medium">$','')
    marketVol = str(marketVol).replace('</div></div>','')
    



    


    #get price
    price = results.find('div', class_='price-large')
    price = str(price).replace('<div class="price-large"><span class="symbol">$</span>','')
    price = str(price).replace('</div>','')
    price = str(price).replace(',','')



    return price, priceChange, marketVol, marketCap, priceChangeUpOrDown




def displayDataScreen(crypto):
    
    console = Console()
    
    price, priceChange, marketVol, marketCap, priceChangeUpOrDown = scrapeRawData(crypto)
    
    console.clear()
    #display crypto message
    if crypto == ("bitcoin"):
        panel = rich.panel.Panel(rich.text.Text(r"""
██████  ██ ████████  ██████  ██████  ██ ███    ██ 
██   ██ ██    ██    ██      ██    ██ ██ ████   ██ 
██████  ██    ██    ██      ██    ██ ██ ██ ██  ██ 
██   ██ ██    ██    ██      ██    ██ ██ ██  ██ ██ 
██████  ██    ██     ██████  ██████  ██ ██   ████ 
""", justify="center"))
        rich.print(panel)
    
        with Progress(
            SpinnerColumn(spinner_name="point",style="point"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Downloading Data...", total=100)
            task2 = progress.add_task("Processing Data...", total=100,start=False)
            task3 = progress.add_task("Thinking...", total=100,start=False)

            while not progress.finished:
                progress.update(task1, advance=random.uniform(0.1,0.3))
                if progress.tasks[0].completed > 100:
                    progress.start_task(task2)
                    progress.update(task2, advance=random.uniform(0.001,0.3))
                if progress.tasks[1].completed > 100:
                    progress.start_task(task3)
                    progress.update(task3, advance=random.uniform(0.1,0.2))
                
                time.sleep(0.02)

        time.sleep(10)
        console.clear()
    
    
    
    
    
    else:
        panel = rich.panel.Panel(rich.text.Text(r"""
███████ ████████ ██   ██ ███████ ██████
██         ██    ██   ██ ██      ██   ██
█████      ██    ███████ █████   ██████
██         ██    ██   ██ ██      ██   ██
███████    ██    ██   ██ ███████ ██   ██ 
""", justify="center"))
        rich.print(panel)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            
            task1 = progress.add_task("Downloading Data...", total=100)
            task2 = progress.add_task("Processing Data...", total=100,start=False)
            task3 = progress.add_task("Thinking...", total=100,start=False)

            while not progress.finished:
                progress.update(task1, advance=random.uniform(0.1,0.3))
                if progress.tasks[0].completed > 100:
                    progress.start_task(task2)
                    progress.update(task2, advance=random.uniform(0.001,0.3))
                if progress.tasks[1].completed > 100:
                    progress.start_task(task3)
                    progress.update(task3, advance=random.uniform(0.1,0.2))
                
                time.sleep(0.02)

       
        time.sleep(10)
    console.clear()

def infoLayout(crypto):
    
    price, priceChange, marketVol, marketCap, priceChangeUpOrDown = scrapeRawData(crypto)
    
    table = Table(show_lines=True,title=crypto)
    
    table.add_column("Statistics",justify="center")
    
    table.add_row("Current Price",price)
    table.add_row("Market Volume",marketVol)
    table.add_row("Market Cap",marketCap)
    
    

    
    




    console = Console()
    console.clear()
    layout = Layout()
    layout.split_column(
        Layout(name="lower"),
    )
    layout["lower"].split_row(
        Layout(Panel.fit(table,title="Statistics?"),name="left"), Layout(Panel.fit(getCRYPTOFact(),title="Did You Know?"),name="right"),
    )
    print("\n")
    rich.print(layout)
    time.sleep(30)


while True:
    getCRYPTOFact()
    displayDataScreen("bitcoin")
    infoLayout("bitcoin")
    getBTC(1)
    displayDataScreen("ethereum")
    infoLayout("ethereum")
    getETH(1)




    
        
    
    
    
