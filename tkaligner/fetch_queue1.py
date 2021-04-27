""" fetch queue1 and restore """

from typing import Any

from queue import Empty, Full, Queue


def fetch_queue1(que: "Queue[Any]", fill=None) -> Any:
    """ fetch queue1 and restore if fill=None
    
    or fetch and fill with fill
    
    >>> from queue import Queue
    >>> q = Queue(1)
    >>> fetch_queue1(q)
    ''
    >>> fetch_queue1(q, 1)
    ''
    >>> fetch_queue1(q)
    1
    """

    try:
        _ = que.get_nowait()
    except Empty:
        _ = ""
    if fill is None:  # can race happen?
        try:
            que.put(_, block=False)
        except Full:
            ...
    else:
        try:
            que.put(fill, block=False)
        except Full:
            ...

    return _
