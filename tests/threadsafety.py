import threading
from queue import Queue

from tidylib import tidy_document

error_queue = Queue()

DOC = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title></title>
  </head>
  <body>
    hello, world
  </body>
</html>
'''

SAMPLE = "hello, world"

NUM_THREADS = 100
NUM_TRIES = 100


class TidyingThread(threading.Thread):
    def run(self):
        for x in range(NUM_TRIES):
            output, errors = tidy_document(SAMPLE, keep_doc=True)
            if output != DOC:
                error_queue.put(output)


def run_test():
    threads = []
    for i in range(NUM_THREADS):
        t = TidyingThread()
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    run_test()
    if not error_queue.empty():
        print("About %s errors out of %s" % (error_queue.qsize(), NUM_THREADS * NUM_TRIES))
        print(error_queue.get())
