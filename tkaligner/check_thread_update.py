""" check thread and update pbar via QUEUE.
Used in association with myprogressbar_ui
"""

# import os
import tkinter as tk
from tkinter import messagebox
from pandas import DataFrame

import blinker
# import logzero
from logzero import logger

from queue import Empty
from queue1_put import queue1_put
from queues import (QUEUE, QUEUE_C, QUEUE_PA, QUEUE_SA, QUEUE_PS,
                    QUEUE_P1, QUEUE_P2, QUEUE_S1, QUEUE_S2,
                    QUEUE_PM, QUEUE_SM)
import myprogressbar_ui_support

SIG_TABLE = blinker.signal("table")

# myprogressbar_ui_support.set_Tk_var()


def check_thread_update(self, thr):
    """ check thread thr and update pbar via QUEUE.

    called in myprogressbar_ui called by paligner/saligner
    self is pbar
    in palign_command:
        pbar = myprogressbar_ui.Mypbar(window)
        [window = tk.Toplevel(top)] / top = self.top / self(aligner)
    """

    pbar = self

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
        # pbar.TProgressbar1.after(500, lambda: check_thread_update(thr, pbar))
        pbar.TProgressbar1.after(500, lambda: check_thread_update(pbar, thr))

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

        # stop the indeterminate progressbar
        pbar.TProgressbar1.stop()
        pbar.TProgressbar1['value'] = 1
        # pbar.TProgressbar1.destroy()  # dose not work

        try:
            flag = QUEUE_PS.get_nowait()
            queue1_put(QUEUE_PS, flag)
        except Empty:
            flag = ""

        # ######### SENTS ###########
        # set QUEUE_PA self.saligned

        if flag in ["s"]:  # activated from salign_command

            # update Table and Pad from bee_aligner.plist_to_slist thread
            # in myprogressbar_ui/start_command

            messagebox.showinfo(" Sent aligning completed!", "You can adjust the threshold and realign or press Back and edit the upper table manually.")

            try:
                s_list = thr.flist  # thr is c_th in plist_to_slist
            except Exception as exc:
                logger.error("s_list = thr.flist exc: %s, maybe thread has not run well or has been attached a different result", exc)

                return None

            logger.debug("s_list: %s", s_list)

            SIG_TABLE.send("check_thread_update", df=s_list)

            # set QUEUE_SA self.saligned
            queue1_put(QUEUE_SA, True)

            # set QUEUE_S1, QUEUE_S2 QUEUE_SM
            df = DataFrame(s_list)
            queue1_put(QUEUE_S1, df[0])
            queue1_put(QUEUE_S2, df[1])
            queue1_put(QUEUE_SM, df[2])

            logger.info("sents aligning completed.")
            logger.debug(" <check_thread_update> exit")

            return None

        # ######### PARAS ###########
        # set QUEUE_PA self.paligned

        # update Table and Pad from bee_aligner.bee_aligner thread
        # in myprogressbar_ui/start_command

        messagebox.showinfo(" Para aligning completed!", "You can adjust the threshold and realign or press Back and edit the upper table manually.")

        para_list = thr.para_list  # thr is c_th in bee_aligner
        SIG_TABLE.send("check_thread_update", df=para_list)

        queue1_put(QUEUE_PA, True)

        # set QUEUE_P1, QUEUE_P2 QUEUE_PM
        df = DataFrame(para_list)
        queue1_put(QUEUE_P1, df[0])
        queue1_put(QUEUE_P2, df[1])
        queue1_put(QUEUE_PM, df[2])

        logger.info("paras aligning completed.")
        logger.debug(" <check_thread_update> exit")
