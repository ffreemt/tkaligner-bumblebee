""" check thread and update pbar via QUEUE.
Used in association with myprogressbar_ui
"""
import os
import tkinter as tk
import logzero
from logzero import logger

from queues import QUEUE, QUEUE_C
import myprogressbar_ui_support

# myprogressbar_ui_support.set_Tk_var()

_ = os.environ.get("ALIGNER_DEBUG")
if _ is not None and (_ == '1' or _.lower() == 'true'):
    logzero.loglevel(10)  # 10: DEBUG, default 20: INFO
else:
    logzero.loglevel(20)

def check_thread_update(thr, pbar):
    """ check thread thr and update pbar via QUEUE. """

    if thr.is_alive():
        logger.debug("+++ check_threa_update %s ++alive++ ", thr.name)

        # pbar.TProgressbar1.step()
        # pbar.TProgressbar1['value'] = thr.value  # this does not update for some weird reason

        # c_value = pbar.TProgressbar1['value']
        # c_value = pbar.TProgressbar1['value']

        # set pbar:
        # pbar.TProgressbar1['value'] = number

        def update_status():
            """ update running label.
            need to reuse this when the thread is terminated
            """
            old_value = pbar.TProgressbar1["value"]
            if QUEUE.qsize():  # pbar queue
                c_value = QUEUE.get_nowait()
                logger.debug("**== check_thread_update QUEUE. c_value: %.2f", c_value)

                step = c_value - old_value
                pbar.TProgressbar1.step(step)

            # counter text queue
            if QUEUE_C.qsize():
                text = QUEUE_C.get_nowait()
                logger.debug("**== check_thread_update QUEUE_C text: %s", text)

                # myprogressbar_ui_support.pbarvar.set(text)
                myprogressbar_ui_support.statustext.set(text)

                # pbar.TLabel1.delete('0.0', 'end')
                # pbar.TLabel1.insert('0.0', text)

        update_status()

        # resursive
        pbar.TProgressbar1.after(500, lambda: check_thread_update(thr, pbar))

    else:
        # update_status()

        logger.debug("*** %s not alive", thr.name)
        logger.debug(
            # "value(pbar): %s：thr.value %s", pbar.TProgressbar1["value"], thr.value
            # thr.value removed, TProgressbar1 fetches value from QUEUE/QUEUE_C
            "value(pbar): %s", pbar.TProgressbar1["value"]
        )

        # extra update after thread exited
        # c_value = pbar.TProgressbar1["value"]
        # step = thr.value - c_value
        # pbar.TProgressbar1.step(step - 0.1)
        # pbar.TProgressbar1.update()

        old_value = pbar.TProgressbar1["value"]
        if QUEUE.qsize():  # pbar queue
            c_value = QUEUE.get_nowait()
            logger.debug("**== check_thread_update QUEUE. c_value: %.2f", c_value)

            step = c_value - old_value
            pbar.TProgressbar1.step(step - 0.1)

        # update running label/statustext
        if QUEUE_C.qsize():
            text = QUEUE_C.get_nowait()
            logger.debug("**== check_thread_update QUEUE_C text: %s", text)

            # myprogressbar_ui_support.pbarvar.set(text)
            myprogressbar_ui_support.statustext.set(text)

        logger.debug(" Restore buttons 1 2 3 states")
        # pbar(self) TButton1: Start, 2: Cancel,3: Back
        pbar.TButton1.config(state=tk.NORMAL)
        pbar.TButton2.config(state=tk.DISABLED)
        pbar.TButton3.config(state=tk.NORMAL)

        # print(pbar.TButton1.config())

        logger.debug(" <check_thread_update> exit")
        # logger.info(" thr.res: **%s**", thr.res)
