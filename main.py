#!/usr/bin/env -S uv run
import requests
from telegram import Bot
from datetime import datetime
import json

# Load configuration from a file (you can set this as a JSON file)
CONFIG_FILE = 'config.json'

# Function to check VAT number validity via the REST API
def check_vat(vat_number: str, country_code: str, requester_member_state_code: str, requester_number: str) -> bool:
    try:
        url = 'https://ec.europa.eu/taxation_customs/vies/rest-api/check-vat-number'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data: dict[str, str] = {
            "countryCode": country_code,
            "vatNumber": vat_number,
            "requesterMemberStateCode": requester_member_state_code,
            "requesterNumber": requester_number
        }

        # Make the request to the VIES REST API
        response = requests.post(url, json=data, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            response_data: dict[str, bool] = response.json()
            if response_data['valid']:
                return True  # VAT number is valid
            else:
                print(f"[{datetime.now()}] VAT {vat_number} is NOT valid.")
                print(f"Response payload: {response_data}")
                return False  # VAT number is not valid
        else:
            print(f"[{datetime.now()}] Failed to validate VAT {vat_number}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to send a message via Telegram
async def send_telegram_message(bot_token: str, chat_id: str, message: str) -> None:
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"[{datetime.now()}] Message sent successfully: {message}")
    except Exception as e:
        print(f"[{datetime.now()}] Failed to send message: {e}")

# Load configuration (Telegram settings, VAT number, etc.)
def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

# Main loop for checking VAT and sending notifications
def main():
    config = load_config()

    vat_number = config['vat_number']
    country_code = config['country_code']
    requester_member_state_code = config['requester_member_state_code']
    requester_number = config['requester_number']

    bot_token = config['telegram_bot_token']
    chat_id = config['telegram_chat_id']

    import asyncio

    async def async_main():
        while True:
            vat_valid = check_vat(vat_number, country_code, requester_member_state_code, requester_number)
            if vat_valid:
                message = f"✨ VAT {vat_number} is now valid!"
                await send_telegram_message(bot_token, chat_id, message)
                break  # Exit loop once VAT is valid
            else:
                message = f"💀 Not valid yet: VAT {vat_number}"
                await send_telegram_message(bot_token, chat_id, message)
            await asyncio.sleep(config.get('check_interval', 60))  # Wait for the specified interval (default: 60 seconds)

    asyncio.run(async_main())

if __name__ == "__main__":
    main()
