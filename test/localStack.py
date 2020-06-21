import threading
import time

from werkzeug.local import LocalStack

my_stack = LocalStack()
my_stack.push(1)
print('In main, value:' + str(my_stack.top))


def worker():
    print('In new thread after, value:' + str(my_stack.top))
    my_stack.push(2)
    print('In new thread before, value:' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='ruansong')
new_t.start()
time.sleep(1)
# 主线程
print('In main, value:' + str(my_stack.top))
