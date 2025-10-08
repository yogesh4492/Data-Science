"""How The Processpollexecuter Work

create a pool of separate process,each with its own python interpreter and memory is separator

each process run truly in parallel
best for cpu-bound tasks
"""

from concurrent.futures import ProcessPoolExecutor

import time
from rich.progress import Progress
import math
import sys
def download_files(file):
    # time.sleep(1)
    return file
    
# sys.set_int_max_str_digits(1000)


files=[x for x in range(1,10000)]
with Progress() as p:
        task=p.add_task("Processing....",total=len(files))
      
        with ProcessPoolExecutor(max_workers=1) as e:
            result=e.map(download_files,files)
            for i in result:
                print(i)
                p.update(task,advance=1)

        