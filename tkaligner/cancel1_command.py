""" """

from queues import QUEUE_S1


def cancel1_command(self):
    """ cancel1 align and destroy pbar. """
    from time import sleep

    logger.debug(" cancel1_command.py ")

    logger.debug("QUEUE_S1.put(True, block=0")

    # QUEUE_S.put(True, block=False)
    queue1_put(QUEUE_S1, True)

    sleep(0.8)  # wait for thread to quit
