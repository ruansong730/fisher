"""
Local线程隔离
"""
import threading
import time

from werkzeug.local import Local


class A:
    b = 1


my_obj = Local()
my_obj.b = 1


def worker():
    # 新线程
    my_obj.b = 2
    print('in new thread b is ' + str(my_obj.b))


new_t = threading.Thread(target=worker, name='ruansong_thread')
new_t.start()
time.sleep(1)
print('in main thread b is ' + str(my_obj.b))
