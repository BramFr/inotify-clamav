import inotify.adapters
from subprocess import run
from threading import Thread

watch_folder = '/path/to/folder'

def _worker(file_path):
    '''
    This function start clamdscan with a new thread. Please give the path of the file.
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
            if 'IN_CREATE' in event[1]:
                (header, type_names, watch_path, filename) = event
                file_path = watch_path + '/' + filename
                Thread(target=_worker, args=({file_path})).start()
                print(f'{file_path}')


if __name__ == '__main__':
    _main()
