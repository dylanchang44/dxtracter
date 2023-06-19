import logging, requests, datetime, yaml, asyncio
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler
from rating import Drater
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load the keys from the YAML file
with open('keys.yml') as file:
    keys = yaml.safe_load(file)

# Your telegram bot token
BOT_TOKEN = keys['BOT_TOKEN']
# Your ALPHA VANTAGE api key
stock_api_key = keys['STOCK_API']
#Default stock symbol
stock_symbol = 'TSLA'

left_request_d = 500 
left_request_m = 5

async def start(update, context):
    start_text = "I'm Dxtracter\nA telegram bot to extract recent infos from company\n\n"
    start_text+=f"Please type-in a valid stock symbol to fetch data\nCrurrent stock symbol => {stock_symbol}\nExample stock symbol => NVDA , AAPL , amd\n(yes small case is also valid)\n\n"
    start_text+="Due to Alpha Vantage standard API usage limit\n(5 API requests per minute; 500 API requests per day)\nIntensive request is not feasible"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Remaining requests:\nDay period - {left_request_d}\nMinute period - {left_request_m}")

async def stock_option(update, context):
    global stock_symbol
    # Update the stock symbol by user type-in
    stock_symbol = update.message.text.upper()  
    # Send the text and options to the user
    info_text=f"Modify stock symbol to << {stock_symbol} >>\n!!! If stock symbol invalid, raise Error when extracting !!!"
    options_text = f"Let's extract the company's info!\n\nOptions:\n"
    options_text += "/start - dxtracter introduction\n"
    options_text += "/getnews - Show 2 recent news for the company (cost 1 api request)\n"
    options_text += "/getrate - Evaluate rating for the company (cost 4 api requests)\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Remaining requests:\nDay period - {left_request_d}\nMinute period - {left_request_m}")


async def get_news(update, context):
    news_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock_symbol}&apikey={stock_api_key}'
    global left_request_d,left_request_m
    left_request_d-=1 
    left_request_m-=1
    try:
        response = requests.get(news_url)
        data = response.json()

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Fetching 2 latest news for the company => {stock_symbol}")
        news_list = data['feed'][:2]  # Get the first two news articles
        for news in news_list:
            message = ""
            
            title = news['title']
            published_time = news['time_published']
            summary = news['summary']
            url = news['url']

            datetime_obj = datetime.datetime.strptime(published_time, "%Y%m%dT%H%M%S") 
            message += f"Company: {stock_symbol}\n\n"
            message += f"Title: {title}\n\n"
            message += datetime_obj.strftime("Date: %Y/%m/%d\n")
            message += datetime_obj.strftime("Time: %H:%M\n\n")
            message += f"Summary:\n{summary}\n\n"
            message += f"{url}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    #http request error handling    
    except Exception as e:
        message += "Error: Failed to send HTTP request.\nPlease check if the stock symbol is correct\n"
        message += "Or if the remaining requests is enough"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Remaining requests:\nDay period - {left_request_d}\nMinute period - {left_request_m}")

async def get_rating(update, context):
    # Load the YAML file (V)
    # fetch data from http request
    # store into target data
    # calculate to fin_data
    # weighted
    with open('data.yml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    stock_rate = Drater()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Fetching the Fundamental Data of the company => {stock_symbol}")
    stock_rate.parse_target(data)

    global left_request_d,left_request_m
    left_request_d-=4
    left_request_m-=4
    try:
        await stock_rate.fetch_data(stock_api_key, stock_symbol)
        rate = stock_rate.rating_calc()
        analysis = (
            "Strong Buy" if rate < 1.5 else
            "Outperform" if rate < 2.5 else
            "Hold" if rate < 3.5 else
            "Underperform" if rate < 4.5 else
            "Strong Sell"
        )
        output_text = f"Based on the last quarterly reports of {stock_symbol}\n\nBuying rating: {rate:.2f}\nAnalysis: {analysis}"
    except Exception as e:
        output_text = "Error: Failed to send HTTP request.\nPlease check if the stock symbol is correct\n"
        output_text+= "Or if the remaining requests is enough"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Remaining requests:\nDay period - {left_request_d}\nMinute period - {left_request_m}")

async def update_counters():
    global left_request_d,left_request_m
    while True:
        # Refresh left_request_d every day
        left_request_d = 500
        for _ in range(1440): #minutes count of a day
            # Refresh left_request_m every minute
            left_request_m = 5
            await asyncio.sleep(60)  # Sleep for 60 seconds

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    symbol_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), stock_option)
    news_handler = CommandHandler('getnews', get_news)
    rate_handler = CommandHandler('getrate', get_rating)

    application.add_handler(start_handler)
    application.add_handler(symbol_handler)
    application.add_handler(news_handler)
    application.add_handler(rate_handler)

    #asyncio.create_task(update_counters())
    loop = asyncio.get_event_loop()
    loop.create_task(update_counters())
    #run bot
    application.run_polling()
    

if __name__ == '__main__':
    main()