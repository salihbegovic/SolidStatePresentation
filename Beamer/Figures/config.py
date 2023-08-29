import matplotlib as mp
import logging
import os
logging.basicConfig(level=logging.INFO)


def source_matplotlib_options():
    conf = os.path.join(os.path.dirname(__file__), "matplotlib.yaml")
    mp.rc_file(conf)
