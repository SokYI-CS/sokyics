import telebot
from pdf2image import convert_from_path
from PIL import Image
import os



# Initialize the bot with your token
bot_token = 'YourAPI'
bot = telebot.TeleBot(bot_token)

# List of authorized chat IDs
authorized_chat_ids = [YourChatID]  # Add more authorized chat IDs to this list

# Function to convert PDF to JPG
def convert_pdf_to_jpg(pdf_path):
    images = convert_from_path(pdf_path, 300)  # 300 DPI for high resolution
    for i, image in enumerate(images):
        jpg_path = f"{pdf_path[:-4]}_{i+1}.jpg"
        image.save(jpg_path, 'JPEG')
    return [f"{pdf_path[:-4]}_{i+1}.jpg" for i in range(len(images))]

# Command to start the bot and provide instructions
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in authorized_chat_ids:
        bot.reply_to(message, "ជម្រាបសួរបង🙏😊 សូមបងផ្ញើរ file PDF មក I'll convert it to high-resolution JPG images.")
    else:
        bot.reply_to(message, "ជម្រាបសួរបង🙏😊, ខ្ញុំបាន Check មើលឃើញថាបងអត់ទាន់មានឈ្មោះក្នុងការប្រើប្រាស់មុខ Covert PDF to រូបភាពទេ​។ សូមបងទាក់ទងទៅកាន់ @AminYaCar Account.")

# Handle document uploads
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.chat.id not in authorized_chat_ids:
        bot.reply_to(message, "We don't know you yet. Please send your chat ID to  Your accout Telegram.")
        return  # Stop processing if user is not authorized

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save PDF to local storage
        pdf_path = f"{message.document.file_name}"
        with open(pdf_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Inform user that conversion is starting
        bot.reply_to(message, "Please wait while I convert your PDF file.")
        
        # Convert PDF to JPG
        if pdf_path.lower().endswith('.pdf'):
            jpg_paths = convert_pdf_to_jpg(pdf_path)
            for jpg_path in jpg_paths:
                photo = open(jpg_path, 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
                os.remove(jpg_path)  # Remove the image after sending
        else:
            bot.reply_to(message, "Please upload a PDF file.")
        
        # Remove the PDF after conversion
        os.remove(pdf_path)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Handle non-document messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.chat.id in authorized_chat_ids:
        bot.reply_to(message, "Please send me a PDF file to convert.")
    else:
        bot.reply_to(message, "We don't know you yet. Please send your chat ID to @YourAcount.")

# Start the bot
bot.polling()
