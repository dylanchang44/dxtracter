import logging, requests, configparser, datetime
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

config = configparser.ConfigParser()    # Define the method to read the configuration file
config.read('config.ini')               # read config.ini file

#Your telegram bot token
BOT_TOKEN = config.get('default','BOT_TOKEN')
#Your ALPHA VANTAGE api key 
stock_api_key = config.get('default','STOCK_API')
#Default stock symbol
stock_symbol = 'TSLA'

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm dxtracter, a bot to extract recent news for a company!\nPlease type a stock symbol for input.")

async def stock_option(update, context):
    global stock_symbol
    # Update the stock symbol by user type-in
    stock_symbol = update.message.text.upper()  
    # Send the options to the user
    options_text = "Options:\n/getnews - show 2 recent news for the company\n/getrate - calculate buying rating for the company"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=options_text)


async def get_news(update, context):
    news_url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock_symbol}&apikey={stock_api_key}'

    response = requests.get(news_url)
    data = response.json()

    if 'Error Message' in data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid stock symbol. Please try again.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Showing 2 latest news of the company")
        news_list = data['feed'][:2]  # Get the first two news articles
        for news in news_list:
            title = news['title']
            published_time = news['time_published']
            summary = news['summary']
            url = news['url']

            datetime_obj = datetime.datetime.strptime(published_time, "%Y%m%dT%H%M%S")


            message = ""
            message += f"Company: {stock_symbol}\n\n"
            message += f"Title: {title}\n\n"
            message += datetime_obj.strftime("Date: %Y/%m/%d\n")
            message += datetime_obj.strftime("Time: %H:%M\n\n")
            message += f"Summary:\n{summary}\n\n"
            message += f"{url}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def get_rating(update, context):
    # Calculate the buying rating for the company using an algorithm or any other method
    rating=3.0
    rating_text = f"The buying rating for {stock_symbol} is {rating}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rating_text)

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

    application.run_polling()

if __name__ == '__main__':
    main()