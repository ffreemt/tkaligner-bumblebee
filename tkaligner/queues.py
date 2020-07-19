"""queues

redesign? 2020 07 08
float: total
bool: True -> stop
int: increamental

# from threading import Thread
from queue import Queue, Full


class QueueLatest(Queue):
    ''' customized put'''
    def put(self, item):
        while True:
            try:
                super().put(item, block=False)
                break
            except Full:
                _ = self.queue.popleft()


class QueueLatest1(Queue):
    ''' customized put
    def put(self,*as,**kwas):
      if 'block' in kwas:
        super().put(*as,**kwas)
      else:
        super().put(block=True,...)
    '''
    def put(self, *args, **kwargs):
        if 'block' not in kwargs:
            kwargs['block'] = False

        try:
            super().put(*args, **kwargs)
        except Full:
            self.queue.popleft()
            super().put(*args, **kwargs)


# QUEUE = Queue(1)
QUEUE = QueueLatest1(1)  # c_value: % value and bool
QUEUE_S = QueueLatest1(1)
# STOP queue for stopping longtime_job thead
QUEUE_C = QueueLatest1(1)  # DATA queue for longtime_job and pbar counter: step
QUEUE_T1 = QueueLatest1(1)  # text1 queue for self.text1
QUEUE_T2 = QueueLatest1(1)  # text2 queue for self.text2
QUEUE_SPINBOX = QueueLatest1(1)  # threshold for the aligner

"""

from queue import Queue

# reimplement sans QueueLatest1
# just use Queue(1), when do q.put(elm) do (get first):
# try: q.get(block=False)
# except Empty: ... finally: q.put(elm)

QUEUE = Queue(1)  # c_value: % value and bool

# STOP queue for stopping longtime_job thead
QUEUE_S = Queue(1)
QUEUE_S1 = Queue(1)

# running label queue for longtime_job and pbar counter: step
QUEUE_C = Queue(1)
QUEUE_T1 = Queue(1)  # text1 queue for self.text1
QUEUE_T2 = Queue(1)  # text2 queue for self.text2
QUEUE_SPINBOX = Queue(1)  # threshold for the aligner

# pylint: disable=invalid-name
queues = [QUEUE, QUEUE_S, QUEUE_C, QUEUE_T1, QUEUE_T2, QUEUE_SPINBOX]
