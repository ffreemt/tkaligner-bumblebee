"""
refactor

imitate long running job
"""

import os
from time import sleep
from threading import currentThread

import blinker
from pandas import DataFrame

import logzero
from logzero import logger

from queues import QUEUE, QUEUE_S, QUEUE_C
from queue1_put import queue1_put

SIG_TABLE = blinker.signal("table")
SIG_PAD = blinker.signal("pad")


def longtime_job(*args, **kwargs):
    """ longtime job.

    QUEUE.put_nowait(percentage completed): numb in %
    QUEUE_C.put_nowait( label ): f"elm/tot"
    .put_nowait replaced by queue1_put: Queue(1), only keeps the most updated content

    exit on QUEUE_S (True)

    """
    longtime_job.res = None

    logger.debug("<longtime_job> entry, kwargs: %s", kwargs)

    # reset QUEUE, QUEUE_S, QUEUE_C
    # QUEUE.put(0, block=False)
    # QUEUE_C.put(0, block=False)

    queue1_put(QUEUE, 0)
    queue1_put(QUEUE_C, 0)

    # run in a thread thr, able to fetch thread related info
    c_thr = currentThread()

    logger.debug(" c_th.ident: %s, c_th.name: %s", c_thr.ident, c_thr.name)

    # c_thr.stop = False  # not used, deleted
    # c_thr.value = 0

    # emitate worker
    # pbar start butt/bind to start_command:
    # run check_thread_update, thread( of longtime_job).start()
    if kwargs.get("counter"):
        try:
            counter = int(kwargs.get("counter"))
        except Exception as exc:
            logger.error("exc: %s", exc)
            counter = 10
    else:
        counter = 10
    for elm in range(counter):
        logger.debug(f"{elm}/{counter}")
        # check QUEUE_S size 1
        queue_s = None if not QUEUE_S.qsize() else QUEUE_S.get_nowait()
        if queue_s:  # QUEUE_S True, quit working
            break

        # sleep(0.5)  # pretending doing work
        sleep(0.2)  # pretending doing work
        # sleep(1.0)  # pretending doing work

        # step = 1 / counter  * 100
        # c_value out of 100 completed
        c_value = (elm + 1) / counter * 100.

        # send to respective QUEUEs
        # QUEUE.put(c_value, block=False)
        # QUEUE_C.put(f"{elm}/{counter}", block=False)
        queue1_put(QUEUE, c_value)
        queue1_put(QUEUE_C, f"{elm + 1}/{counter}")

    # for ... break ... else
    else:  # if break does not occur/loop completed
        logger.debug("<<longtime_job>> exit")

        # normal exit, reset pbar
        c_value = 0  # reset pbar

        longtime_job.res = "normal return result"
        c_thr.res = "normal return result"

        df = DataFrame(zip([1, 1, 1], [0, 0, 0], ['']*3), columns= ['text1', 'text2', 'merit'])
        # logger.info("SIG_PAD.send(\"job\", df=df: %s,)", df)

        SIG_TABLE.send("job", df=df)
        # SIG_PAD.send("job", df=df)

        return None  # normal function return

    # break does occur
    c_thr.res = ""

    logger.debug("breaking..., reset progressbar")
    c_value = 0  # reset pbar

    # QUEUE.put(0, block=False)
    # QUEUE_C.put(f"{0}/{counter}", block=False)

    queue1_put(QUEUE, 0)
    queue1_put(QUEUE_C, f"{0}/{counter}")

    # TProgressbar1 wont update after a cancel
    # need to use step(step_value)
    # Use destroy pbar in cancel_command
