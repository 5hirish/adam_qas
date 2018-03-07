import os
import sys
import logging

"""
Created by felix on 8/3/18 at 1:39 AM
"""

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        arguments = sys.argv

    else:
        raise ValueError('Missing Arguments')