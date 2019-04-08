#!/usr/bin/env python3
from subprocess import run
from threading import Thread
import inotify.adapters

watch_folder = '/path/to/folder'
inotify_event = ('IN_CREATE', 'IN_MODIFY', 'IN_ATTRIB')
'''
EVENT SYMBOLS

These basic event mask symbols are defined:

IN_ACCESS          File was accessed (read) (*)
IN_ATTRIB          Metadata changed (permissions, timestamps, extended
                   attributes, etc.) (*)
IN_CLOSE_WRITE     File opened for writing was closed (*)
IN_CLOSE_NOWRITE   File not opened for writing was closed (*)
IN_CREATE          File/directory created in watched directory (*)
IN_DELETE          File/directory deleted from watched directory (*)
IN_DELETE_SELF     Watched file/directory was itself deleted
IN_MODIFY          File was modified (*)
IN_MOVE_SELF       Watched file/directory was itself moved
IN_MOVED_FROM      File moved out of watched directory (*)
IN_MOVED_TO        File moved into watched directory (*)
IN_OPEN            File was opened (*)
'''


def _worker(file_path):
    '''
    This function start clamdscan with a new thread. Five the path of the folder.
    '''
    run_command = ['/usr/bin/clamdscan', '--fdpass', '--remove=yes', file_path]
    run(run_command)


def _main():
    try:
        i = inotify.adapters.InotifyTree(watch_folder)
    except PermissionError:
        print(f'Please start script with enough permissons')

    for event in i.event_gen():
        if event is not None:
            if event[1][0] in inotify_event:
                (header, type_names, watch_path, filename) = event
                file_path = watch_path + '/' + filename
                Thread(target=_worker, args=({file_path})).start()
                print(f'{file_path}')


if __name__ == '__main__':
    _main()
