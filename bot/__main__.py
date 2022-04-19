from signal import signal, SIGINT
from os import path as ospath, remove as osremove, execl as osexecl
from subprocess import run as srun, check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from pyrogram import idle
from sys import executable
from telegram import ParseMode, InlineKeyboardMarkup
from telegram.ext import CommandHandler

from bot import bot, app, dispatcher, updater, botStartTime, IGNORE_PENDING_REQUESTS, alive, AUTHORIZED_CHATS, LOGGER, Interval, rss_session
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, sendLogFile
from .helper.ext_utils.telegraph_helper import telegraph
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, delete, count, leech_settings, search, rss


def stats(update, context):
    if ospath.exists('.git'):
        last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd <b>From</b> %cr'"], shell=True).decode()
    else:
        last_commit = 'No UPSTREAM_REPO'
    currentTime = get_readable_time(time() - botStartTime)
    osUptime = get_readable_time(time() - boot_time())
    total, used, free, disk= disk_usage('/')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(net_io_counters().bytes_sent)
    recv = get_readable_file_size(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    stats = f'<b>╭───《⟹ʜᴇɴᴛᴀɪ⟸》</b> {last_commit}\n'\
            f'<b>├─ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:</b> {currentTime}\n'\
            f'<b>├─ᴏꜱ ᴜᴘᴛɪᴍᴇ:</b> {osUptime}\n'\
            f'<b>├─📀ᴛᴏᴛᴀʟ ᴅɪꜱᴋ ꜱᴘᴀᴄᴇ:</b> {total}\n'\
            f'<b>├─💽ᴜꜱᴇᴅ:</b> {used} | <b>Free:</b> {free}\n'\
            f'<b>├─📤ᴜᴘʟᴏᴀᴅ:</b> {sent}\n'\
            f'<b>├─📥ᴅᴏᴡɴʟᴏᴀᴅ:</b> {recv}\n'\
            f'<b>├─💻ᴄᴘᴜ:</b> {cpuUsage}%\n'\
            f'<b>├─💾ʀᴀᴍ:</b> {mem_p}%\n'\
            f'<b>├─💿ᴅɪꜱᴋ:</b> {disk}%\n'\
            f'<b>├─♦️ᴘʜʏꜱɪᴄᴀʟ ᴄᴏʀᴇꜱ:</b> {p_core}\n'\
            f'<b>├─♦️ᴛᴏᴛᴀʟ ᴄᴏʀᴇꜱ:</b> {t_core}\n'\
            f'<b>├─⚠️ꜱᴡᴀᴘ:</b> {swap_t} | <b>ᴜꜱᴇᴅ:</b> {swap_p}%\n'\
            f'<b>├─💾ᴍᴇᴍᴏʀʏ ᴛᴏᴛᴀʟ:</b> {mem_t}\n'\
            f'<b>├─ᴍᴇᴍᴏʀʏ ꜰʀᴇᴇ:</b> {mem_a}\n'\
            f'<b>╰───ᴍᴇᴍᴏʀʏ ᴜꜱᴇᴅ:</b> {mem_u}\n'
    sendMessage(stats, context.bot, update.message)


def start(update, context):
    buttons = ButtonMaker()
    buttons.buildbutton("ᴄʀᴇᴀᴛᴏʀ", "https://t.me/imhurad")
    buttons.buildbutton("ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛ", "https://t.me/RoBot3ir")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
ᴛʜɪꜱ ʙᴏᴛ ᴄᴀɴ ᴍɪʀʀᴏʀ ᴀʟʟ ʏᴏᴜʀ ʟɪɴᴋꜱ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ!
ᴛʏᴘᴇ /{BotCommands.HelpCommand} ᴛᴏ ɢᴇᴛ ᴀ ʟɪꜱᴛ ᴏꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ
'''
        sendMarkup(start_string, context.bot, update.message, reply_markup)
    else:
        sendMarkup('ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀ, ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ᴍɪʀʀᴏʀ-ʟᴇᴇᴄʜ ʙᴏᴛ', context.bot, update.message, reply_markup)

def restart(update, context):
    restart_message = sendMessage("ʀᴇꜱᴛᴀʀᴛɪɴɢ...", context.bot, update.message)
    if Interval:
        Interval[0].cancel()
    alive.kill()
    srun(["pkill", "-f", "gunicorn"])
    clean_all()
    srun(["pkill", "-f", "aria2c"])
    srun(["python3", "update.py"])
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    osexecl(executable, executable, "-m", "bot")


def ping(update, context):
    start_time = int(round(time() * 1000))
    reply = sendMessage("ꜱᴛᴀʀᴛɪɴɢ ᴘɪɴɢ", context.bot, update.message)
    end_time = int(round(time() * 1000))
    editMessage(f'{end_time - start_time} ᴍꜱ', reply)


def log(update, context):
    sendLogFile(context.bot, update.message)


help_string_telegraph = f'''<br>
<b>/{BotCommands.HelpCommand}</b>: ᴛᴏ ɢᴇᴛ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ
<br><br>
<b>/{BotCommands.MirrorCommand}</b> [download_url][magnet_link]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ. ꜱᴇɴᴅ <b>/{BotCommands.MirrorCommand}</b> ꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ
<br><br>
<b>/{BotCommands.ZipMirrorCommand}</b> [download_url][magnet_link]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴇxᴛʀᴀᴄᴛᴇᴅ ꜰʀᴏᴍ ᴀɴʏ ᴀʀᴄʜɪᴠᴇ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.QbMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ, ᴜꜱᴇ <b>/{BotCommands.QbMirrorCommand} s</b> ᴛᴏ ꜱᴇʟᴇᴄᴛ ꜰɪʟᴇꜱ ʙᴇꜰᴏʀᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ
<br><br>
<b>/{BotCommands.QbZipMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴄᴏᴍᴘʀᴇꜱꜱᴇᴅ ᴡɪᴛʜ ᴢɪᴘ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.QbUnzipMirrorCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ᴍɪʀʀᴏʀɪɴɢ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴇxᴛʀᴀᴄᴛᴇᴅ ꜰʀᴏᴍ ᴀɴʏ ᴀʀᴄʜɪᴠᴇ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.LeechCommand}</b> [download_url][magnet_link]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ, ᴜꜱᴇ <b>/{BotCommands.LeechCommand} s</b> ᴛᴏ ꜱᴇʟᴇᴄᴛ ꜰɪʟᴇꜱ ʙᴇꜰᴏʀᴇ ʟᴇᴇᴄʜɪɴɢ
<br><br>
<b>/{BotCommands.ZipLeechCommand}</b> [download_url][magnet_link]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴄᴏᴍᴘʀᴇꜱꜱᴇᴅ ᴡɪᴛʜ ᴢɪᴘ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.UnzipLeechCommand}</b> [download_url][magnet_link][torent_file]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴇxᴛʀᴀᴄᴛᴇᴅ ꜰʀᴏᴍ ᴀɴʏ ᴀʀᴄʜɪᴠᴇ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.QbLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ, ᴜꜱᴇ <b>/{BotCommands.QbLeechCommand} s</b> ᴛᴏ ꜱᴇʟᴇᴄᴛ ꜰɪʟᴇꜱ ʙᴇꜰᴏʀᴇ ʟᴇᴇᴄʜɪɴɢ
<br><br>
<b>/{BotCommands.QbZipLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴄᴏᴍᴘʀᴇꜱꜱᴇᴅ ᴡɪᴛʜ ᴢɪᴘ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.QbUnzipLeechCommand}</b> [magnet_link][torrent_file][torrent_file_url]: ꜱᴛᴀʀᴛ ʟᴇᴇᴄʜɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴇxᴛʀᴀᴄᴛᴇᴅ ꜰʀᴏᴍ ᴀɴʏ ᴀʀᴄʜɪᴠᴇ ᴇxᴛᴇɴꜱɪᴏɴ
<br><br>
<b>/{BotCommands.CloneCommand}</b> [drive_url][gdtot_url]: ᴄᴏᴘʏ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴛᴏ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ
<br><br>
<b>/{BotCommands.CountCommand}</b> [drive_url][gdtot_url]: ᴄᴏᴜɴᴛ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴏꜰ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ
<br><br>
<b>/{BotCommands.DeleteCommand}</b> [drive_url]: ᴅᴇʟᴇᴛᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ꜰʀᴏᴍ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ (ᴏɴʟʏ ᴏᴡɴᴇʀ & ꜱᴜᴅᴏ)
<br><br>
<b>/{BotCommands.WatchCommand}</b> [yt-dlp supported link]: ᴍɪʀʀᴏʀ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ. ꜱᴇɴᴅ <b>/{BotCommands.WatchCommand}</b> ꜰᴏʀ ᴍᴏʀᴇ ʜᴇʟᴘ
<br><br>
<b>/{BotCommands.ZipWatchCommand}</b> [yt-dlp supported link]: ᴍɪʀʀᴏʀ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ ᴀꜱ ᴢɪᴘ
<br><br>
<b>/{BotCommands.LeechWatchCommand}</b> [yt-dlp supported link]: ʟᴇᴇᴄʜ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ
<br><br>
<b>/{BotCommands.LeechZipWatchCommand}</b> [yt-dlp supported link]: ʟᴇᴇᴄʜ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ ᴀꜱ ᴢɪᴘ
<br><br>
<b>/{BotCommands.LeechSetCommand}</b>: ʟᴇᴇᴄʜ ꜱᴇᴛᴛɪɴɢꜱ
<br><br>
<b>/{BotCommands.SetThumbCommand}</b>: ʀᴇᴘʟʏ ᴘʜᴏᴛᴏ ᴛᴏ ꜱᴇᴛ ɪᴛ ᴀꜱ ᴛʜᴜᴍʙɴᴀɪʟ
<br><br>
<b>/{BotCommands.RssListCommand}</b>: ʟɪꜱᴛ ᴀʟʟ ꜱᴜʙꜱᴄʀɪʙᴇᴅ ʀꜱꜱ ꜰᴇᴇᴅ ɪɴꜰᴏo
<br><br>
<b>/{BotCommands.RssGetCommand}</b>: [Title] [Number](last N links): ꜰᴏʀᴄᴇ ꜰᴇᴛᴄʜ ʟᴀꜱᴛ ɴ ʟɪɴᴋꜱ
<br><br>
<b>/{BotCommands.RssSubCommand}</b>: [Title] [Rss Link] f: [filter]: ꜱᴜʙꜱᴄʀɪʙᴇ ɴᴇᴡ ʀꜱꜱ ꜰᴇᴇᴅ
<br><br>
<b>/{BotCommands.RssUnSubCommand}</b>: [Title]: ᴜɴᴜʙꜱᴄʀɪʙᴇ ʀꜱꜱ ꜰᴇᴇᴅ ʙʏ ᴛɪᴛʟᴇ
<br><br>
<b>/{BotCommands.RssSettingsCommand}</b>: ʀꜱꜱ ꜱᴇᴛᴛɪɴɢꜱ
<br><br>
<b>/{BotCommands.CancelMirror}</b>: ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ʙʏ ᴡʜɪᴄʜ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴡᴀꜱ ɪɴɪᴛɪᴀᴛᴇᴅ ᴀɴᴅ ᴛʜᴀᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪʟʟ ʙᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ
<br><br>
<b>/{BotCommands.CancelAllCommand}</b>: ᴄᴀɴᴄᴇʟ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴀꜱᴋꜱ
<br><br>
<b>/{BotCommands.ListCommand}</b> [query]: ꜱᴇᴀʀᴄʜ ɪɴ ɢᴏᴏɢʟᴇ ᴅʀɪᴠᴇ(ꜱ)
<br><br>
<b>/{BotCommands.SearchCommand}</b> [query]: ꜱᴇᴀʀᴄʜ ꜰᴏʀ ᴛᴏʀʀᴇɴᴛꜱ ᴡɪᴛʜ ᴀᴘɪ
<ʙʀ>ꜱɪᴛᴇꜱ: <ᴄᴏᴅᴇ>ʀᴀʀʙɢ, 1337x, ʏᴛꜱ, ᴇᴛᴢᴠ, ᴛɢx, ᴛᴏʀʟᴏᴄᴋ, ᴘɪʀᴀᴛᴇʙᴀʏ, ɴʏᴀᴀꜱɪ, ᴇᴛᴛᴠ<ʙʀ><ʙʀ>
<b>/{BotCommands.StatusCommand}</b>: ꜱʜᴏᴡꜱ ᴀ ꜱᴛᴀᴛᴜꜱ ᴏꜰ ᴀʟʟ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅꜱ
<br><br>
<b>/{BotCommands.StatsCommand}</b>: ꜱʜᴏᴡ ꜱᴛᴀᴛꜱ ᴏꜰ ᴛʜᴇ ᴍᴀᴄʜɪɴᴇ ᴛʜᴇ ʙᴏᴛ ɪꜱ ʜᴏꜱᴛᴇᴅ ᴏɴ
'''

help = telegraph.create_page(
        title='ᴍɪʀʀᴏʀ-ʟᴇᴇᴄʜ-ʙᴏᴛ ʜᴇʟᴘ',
        content=help_string_telegraph,
    )["path"]

help_string = f'''
/{BotCommands.PingCommand}: ᴄʜᴇᴄᴋ ʜᴏᴡ ʟᴏɴɢ ɪᴛ ᴛᴀᴋᴇꜱ ᴛᴏ ᴘɪɴɢ ᴛʜᴇ ʙᴏᴛ
/{BotCommands.AuthorizeCommand}: ᴀᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴄʜᴀᴛ ᴏʀ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ (ᴄᴀɴ ᴏɴʟʏ ʙᴇ ɪɴᴠᴏᴋᴇᴅ ʙʏ ᴏᴡɴᴇʀ & ꜱᴜᴅᴏ ᴏꜰ ᴛʜᴇ ʙᴏᴛ)
/{BotCommands.UnAuthorizeCommand}:ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴄʜᴀᴛ ᴏʀ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ (ᴄᴀɴ ᴏɴʟʏ ʙᴇ ɪɴᴠᴏᴋᴇᴅ ʙʏ ᴏᴡɴᴇʀ & ꜱᴜᴅᴏ ᴏꜰ ᴛʜᴇ ʙᴏᴛ)
/{BotCommands.AuthorizedUsersCommand}: ꜱʜᴏᴡ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ (ᴏɴʟʏ ᴏᴡɴᴇʀ & ꜱᴜᴅᴏ)
/{BotCommands.AddSudoCommand}: ᴀᴅᴅ ꜱᴜᴅᴏ ᴜꜱᴇʀ (ᴏɴʟʏ ᴏᴡɴᴇʀ)
/{BotCommands.RmSudoCommand}: ʀᴇᴍᴏᴠᴇ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ (ᴏɴʟʏ ᴏᴡɴᴇʀ)
/{BotCommands.RestartCommand}: ʀᴇꜱᴛᴀʀᴛ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ʙᴏᴛ
/{BotCommands.LogCommand}: ɢᴇᴛ ᴀ ʟᴏɢ ꜰɪʟᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ. ʜᴀɴᴅʏ ꜰᴏʀ ɢᴇᴛᴛɪɴɢ ᴄʀᴀꜱʜ ʀᴇᴘᴏʀᴛꜱ
/{BotCommands.ShellCommand}: ʀᴜɴ ᴄᴏᴍᴍᴀɴᴅꜱ ɪɴ ꜱʜᴇʟʟ (ᴏɴʟʏ ᴏᴡɴᴇʀ)
/{BotCommands.ExecHelpCommand}: ɢᴇᴛ ʜᴇʟᴘ ꜰᴏʀ ᴇxᴇᴄᴜᴛᴏʀ ᴍᴏᴅᴜʟᴇ (ᴏɴʟʏ ᴏᴡɴᴇʀ)
'''

def bot_help(update, context):
    button = ButtonMaker()
    button.buildbutton("ᴏᴛʜᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ", f"https://telegra.ph/{help}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update.message, reply_markup)

botcmds = [

        (f'{BotCommands.MirrorCommand}', 'ᴍɪʀʀᴏʀ'),
        (f'{BotCommands.ZipMirrorCommand}','ᴍɪʀʀᴏʀ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴀꜱ ᴢɪᴘ'),
        (f'{BotCommands.UnzipMirrorCommand}','ᴍɪʀʀᴏʀ ᴀɴᴅ ᴇxᴛʀᴀᴄᴛ ꜰɪʟᴇꜱ'),
        (f'{BotCommands.QbMirrorCommand}','ᴍɪʀʀᴏʀ ᴛᴏʀʀᴇɴᴛ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ'),
        (f'{BotCommands.QbZipMirrorCommand}','ᴍɪʀʀᴏʀ ᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴀꜱ ᴢɪᴘ ᴜꜱɪɴɢ Qʙ'),
        (f'{BotCommands.QbUnzipMirrorCommand}','ᴍɪʀʀᴏʀ ᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴇxᴛʀᴀᴄᴛ ꜰɪʟᴇꜱ ᴜꜱɪɴɢ Qʙ'),
        (f'{BotCommands.WatchCommand}','ᴍɪʀʀᴏʀ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ'),
        (f'{BotCommands.ZipWatchCommand}','ᴍɪʀʀᴏʀ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ ᴀꜱ ᴢɪᴘ'),
        (f'{BotCommands.CloneCommand}','ᴄᴏᴘʏ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴛᴏ ᴅʀɪᴠᴇ'),
        (f'{BotCommands.LeechCommand}','ʟᴇᴇᴄʜ'),
        (f'{BotCommands.ZipLeechCommand}','ʟᴇᴇᴄʜ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴀꜱ ᴢɪᴘ'),
        (f'{BotCommands.UnzipLeechCommand}','ʟᴇᴇᴄʜ ᴀɴᴅ ᴇxᴛʀᴀᴄᴛ ꜰɪʟᴇꜱ'),
        (f'{BotCommands.QbLeechCommand}','ʟᴇᴇᴄʜ ᴛᴏʀʀᴇɴᴛ ᴜꜱɪɴɢ Qʙɪᴛᴛᴏʀʀᴇɴᴛ'),
        (f'{BotCommands.QbZipLeechCommand}','ʟᴇᴇᴄʜ ᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴜᴘʟᴏᴀᴅ ᴀꜱ ᴢɪᴘ ᴜꜱɪɴɢ Qʙ'),
        (f'{BotCommands.QbUnzipLeechCommand}','ʟᴇᴇᴄʜ ᴛᴏʀʀᴇɴᴛ ᴀɴᴅ ᴇxᴛʀᴀᴄᴛ ᴜꜱɪɴɢ Qʙ'),
        (f'{BotCommands.LeechWatchCommand}','ʟᴇᴇᴄʜ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ'),
        (f'{BotCommands.LeechZipWatchCommand}','ʟᴇᴇᴄʜ ʏᴛ-ᴅʟᴘ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋ ᴀꜱ ᴢɪᴘ'),
        (f'{BotCommands.CountCommand}','ᴄᴏᴜɴᴛ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ᴏꜰ ᴅʀɪᴠᴇ'),
        (f'{BotCommands.DeleteCommand}','ᴅᴇʟᴇᴛᴇ ꜰɪʟᴇ/ꜰᴏʟᴅᴇʀ ꜰʀᴏᴍ ᴅʀɪᴠᴇ'),
        (f'{BotCommands.CancelMirror}','ᴄᴀɴᴄᴇʟ ᴀ ᴛᴀꜱᴋ'),
        (f'{BotCommands.CancelAllCommand}','ᴄᴀɴᴄᴇʟ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛᴀꜱᴋꜱ'),
        (f'{BotCommands.ListCommand}','ꜱᴇᴀʀᴄʜ ɪɴ ᴅʀɪᴠᴇ'),
        (f'{BotCommands.LeechSetCommand}','ʟᴇᴇᴄʜ ꜱᴇᴛᴛɪɴɢꜱ'),
        (f'{BotCommands.SetThumbCommand}','ꜱᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ'),
        (f'{BotCommands.StatusCommand}','ɢᴇᴛ ᴍɪʀʀᴏʀ ꜱᴛᴀᴛᴜꜱ ᴍᴇꜱꜱᴀɢᴇ'),
        (f'{BotCommands.StatsCommand}','ʙᴏᴛ ᴜꜱᴀɢᴇ ꜱᴛᴀᴛꜱ'),
        (f'{BotCommands.PingCommand}','ᴘɪɴɢ ᴛʜᴇ ʙᴏᴛ'),
        (f'{BotCommands.RestartCommand}','ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ'),
        (f'{BotCommands.LogCommand}','ɢᴇᴛ ᴛʜᴇ ʙᴏᴛ ʟᴏɢ'),
        (f'{BotCommands.HelpCommand}','ɢᴇᴛ ᴅᴇᴛᴀɪʟᴇᴅ ʜᴇʟᴘ')
    ]

def main():
    # bot.set_my_commands(botcmds)
    start_cleanup()
    # Check if the bot is restarting
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("ʀᴇꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!", chat_id, msg_id)
        osremove(".restartmsg")
    elif AUTHORIZED_CHATS:
        try:
            for i in AUTHORIZED_CHATS:
                if str(i).startswith('-'):
                    bot.sendMessage(chat_id=i, text="<b>ʙᴏᴛ ꜱᴛᴀʀᴛᴇᴅ!</b>", parse_mode=ParseMode.HTML)
        except Exception as e:
            LOGGER.error(e)

    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("ʙᴏᴛ ꜱᴛᴀʀᴛᴇᴅ!")
    signal(SIGINT, exit_clean_up)
    if rss_session is not None:
        rss_session.start()

app.start()
main()
idle()
