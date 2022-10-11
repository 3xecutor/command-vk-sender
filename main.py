import os
import subprocess
import sys
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from watchdog.observers.polling import PollingObserverVFS
from watchdog.events import PatternMatchingEventHandler

vkToken = ""

vk_session = vk_api.VkApi(token=vkToken)
longpoll = VkLongPoll(vk_session)
api = vk_session.get_api()


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, target_dir, **kwargs):
        PatternMatchingEventHandler.__init__(self, **kwargs)
        self._target_dir = target_dir


    def msg_send(self, id, text):
        vk_session.method('messages.send', {'peer_id': id, 'message': text, 'random_id': 0})

    def send(self, id, text):
        self.msg_send(id, text)

    def on_modified(self, event):
        command = subprocess.check_output("cat .bash_history | tail -n1", shell=True).strip()
        com = "Ого! Новая команда на хосте: " + "\n" + str(command)
        self.send(2000000004, com)




if __name__ == '__main__':
    args = sys.argv[1:]
    source_dir = args[0] if len(sys.argv) > 1 else '.'
    target_dir = args[1] if len(sys.argv) > 1 else '..'

    observer = PollingObserverVFS(stat=os.stat, listdir=os.listdir, polling_interval=1)
    observer.schedule(MyHandler(target_dir, patterns=['.bash_history']),
                      path=source_dir)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()