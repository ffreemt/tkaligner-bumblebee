""" Queue(1) put.

for refactored queues
"""

from typing import Any

from queue import Queue, Empty
from logzero import logger


def queue1_put(que: Queue, elm: Any) -> bool:
    """ Queue(1) (single value queue) put

    keep the most update item

    shorthand for refactored queues

    should hav used deq = deque([], 1)? deq[0], deq.append(...)
    much simpler
    """
    try:
        que.get(block=False)
    except Empty:
        ...
    except Exception as exc:
        logger.error(" que.get exc: %s", exc)
        res = False
    finally:
        que.put(elm, block=False)
        res = True

    return res
