import sys

sys.path.append('..')
import audiosave


def call(args):
    sys.argv = ['wrapper.py']

    keys = args.keys()
    if 'codec' in keys:
        sys.argv.append('--codec')
        sys.argv.append(args['codec'])
    if 'bitrate' in keys:
        sys.argv.append('--bitrate')
        sys.argv.append(args['bitrate'])
    if 'dir' in keys:
        sys.argv.append('--dir')
        sys.argv.append(args['dir'])
    if 'verbose' in keys:
        sys.argv.append('--verbose')
    if 'url' in keys:
        sys.argv.append(args['url'])

    rc = audiosave.main()
    print('done with code', rc, 'but returning 42')
    return 42
