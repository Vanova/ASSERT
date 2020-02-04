from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import utils
import config as cfg

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def do_start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Hello! Greetings!'
    )


def do_echo(bot, update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text='You texted me: "%s"' % text
    )


def do_photo(bot, update):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')
    bot.send_message(chat_id=update.message.chat_id,
                     text='Great! Thanks for the photo!')
    logger.info("Photo of %s: %s", user.first_name, 'photo.jpg')


def do_voice(bot, update):
    user = update.message.from_user
    fid = update.message.voice.file_id
    file = bot.get_file(fid)
    fname = '{}.ogg'.format(fid)
    file.download(fname)

    bot.send_message(chat_id=update.message.chat_id,
                     text='Great! Thanks for the voice message!')
    logger.info('Voice of %s: %s', user.username, fname)

    res = utils.detect_spoofing(fname)
    bot.send_message(chat_id=update.message.chat_id,
                     text='Result:\n%s' % str(res))


def main():
    bot = Bot(token=cfg.TOKEN)
    updater = Updater(bot=bot)

    start_handler = CommandHandler('start', do_start)
    msg_handler = MessageHandler(Filters.text, do_echo)
    ph_handler = MessageHandler(Filters.photo, do_photo)
    voice_handler = MessageHandler(Filters.voice, do_voice)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(msg_handler)
    updater.dispatcher.add_handler(ph_handler)
    updater.dispatcher.add_handler(voice_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
