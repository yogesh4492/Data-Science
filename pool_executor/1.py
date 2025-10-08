""" Difference between ThreadpoolExecutor and ProcessPoolExecutor """

""" Threadpool Executor mainly work with api network ,call 

its work by sharing same memory with thread its switch the thread between max_Worker of the thread pool
- its use when downloading or working with large files and also with api
- its use to reduce time and when work parallry


 """


from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from rich.progress import Progress
import time

def download_files(name):
    print(f"Downloading... {name}")
    time.sleep(2)
    print(f"Finished... {name}")


files=[x for x in range(1,1000)]
with Progress() as p:
    tsk=p.add_task("Processing...",total=len(files))
    with ThreadPoolExecutor(max_workers=32) as e:
        future=e.map(download_files,files)
        for i in future:
            p.update(tsk,advance=1)


    


