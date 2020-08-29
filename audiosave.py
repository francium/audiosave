#!/usr/bin/env python3


"""
Error Codes:
  0       Success
  -1      youtube_dl error
  -2      file_exists_ no_overwrite
"""


import argparse
import os
import youtube_dl


APP_NAME = 'audiosave'
OUTPUT_EXT = {
    'vorbis': '.ogg',
    'mp3': '.mp3'
}

if os.path.isfile('/usr/share/icons/gnome/32x32/mimetypes/audio-x-generic.png'):
    ICON_SUCCESS = '/usr/share/icons/gnome/32x32/mimetypes/audio-x-generic.png'
else:
    ICON_SUCCESS = None

if os.path.isfile('/usr/share/icons/gnome/32x32/status/error.png'):
    ICON_FAILURE = '/usr/share/icons/gnome/32x32/status/error.png'
else:
    ICON_FAILURE = None


def yesno(msg: str) -> bool:
    choice = ''
    while choice.lower() not in ['y', 'n', 'yes', 'no']:
        choice = input(msg.strip() + ' ')

    return True if choice[0].lower() == 'y' else False


def coloredText(message: str, type: str) -> str:
    try:
        from termcolor import colored
    except ModuleNotFoundError:
        # TODO Manually construct message with ANSI/VT100 CODES
        return message

    if type == 'success':
        return colored(message, 'green')  # type: str
    elif type == 'error':
        return colored(message, 'red')  # type: str
    else:
        return message


def notify(title, body=None, icon=None):
    try:
        import gi
        gi.require_version('Notify', '0.7')
        from gi.repository import Notify
        from gi.repository import GdkPixbuf
    except:
        pass

    Notify.init(APP_NAME)
    notification = Notify.Notification.new(title, body)

    if icon:
        image = GdkPixbuf.Pixbuf.new_from_file(icon)
        notification.set_icon_from_pixbuf(image)
        notification.set_image_from_pixbuf(image)

    notification.show()
    Notify.uninit()


def create_dir(dir_path: str) -> None:
    os.makedirs(dir_path)


def move_file(from_, to):
    os.rename(from_, to)

def check_dir_exists(dir_path: str) -> bool:
    return os.path.isdir(dir_path)


def check_file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def download(url: str, codec: str, bitrate: int, title: str = None, quiet: bool = True, force: bool = False):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': str(bitrate),
        }],
        'outtmpl': '%(title)s.%(etx)s',
        'quiet': quiet
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if title is None:
            title = info['title']

        if check_file_exists(title + OUTPUT_EXT[codec]) and not force:
            if yesno('"{}{}" already exists, overwrite it? (y/n)'.format(title, OUTPUT_EXT[codec])):
                overwrite = True
            else:
                overwrite = False
        else:
            overwrite = True

        if overwrite:
            # youtube-dl doesn't seem to raise exceptions (further testing
            # is needed)
            try:
                print("Downloading...")
                status = ydl.download([url])
            except:
                status = -1

            move_file(info.get('title', None) + OUTPUT_EXT[codec],
                      title + OUTPUT_EXT[codec])
            return {'status': status, 'info': info}
        else:
            return {'status': -2}


def parse_args():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('url', help='URL')

    # Primary
    arg_parser.add_argument('-d', '--dir', help='Save directory')
    arg_parser.add_argument('-t', '--title',
                            help='Override filename (minus extension) (default\'s to video title)')

    # Media
    arg_parser.add_argument('--bitrate', default=192, help='Bitrate')
    arg_parser.add_argument('--codec', default='mp3',
                            help='Audio codec (see youtube-dl supported codecs)')

    # Extra
    arg_parser.add_argument('-f', '--force', action='store_true',
                            help='Overwrite existing')
    arg_parser.add_argument('--notify', action='store_true',
                            help='Show notification')
    arg_parser.add_argument('-v', '--verbose', action='store_true',
                            help='Show all output')
    return arg_parser.parse_args()


def handle_download(result, codec: str, show_notif: bool = True) -> None:
    status = result['status']
    if status != -2:
        title = result['info'].get('title', None)
        msg = 'Downloaded "{}{}"'.format(title, OUTPUT_EXT[codec])
    else:
        msg = 'Unknown error'

    if status == 0:
        print(coloredText(msg, 'success'))
        if show_notif:
            notify(msg, icon=ICON_SUCCESS)
        return 0
    if status == -2:
        return 0
    else:
        msg_title = 'Download failed for "{}{}"'.format(title, OUTPUT_EXT[codec])
        msg_body = 'Error {}'.format(status)
        print(coloredText(msg_title, 'error'))
        print(msg_body)

        if show_notif:
            notify(msg_title, msg_body, icon=ICON_FAILURE)

        return status


def main():
    args = parse_args()

    if args.dir:
        if not check_dir_exists(args.dir):
            if yesno(f'{args.dir} does not exist. Create it?'):
                create_dir(args.dir)
        os.chdir(args.dir)

    result = download(args.url, codec=args.codec, bitrate=args.bitrate,
                      title=args.title, quiet=not(args.verbose), force=args.force)
    handle_download(result, args.codec, args.notify)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
