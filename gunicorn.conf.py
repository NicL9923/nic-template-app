import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv(override=True)

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

if not os.getenv("RUNNING_IN_PRODUCTION"):
    reload = True

num_cpus = multiprocessing.cpu_count()
workers = (num_cpus * 2) + 1
worker_class = "uvicorn_worker.UvicornWorker"
control_socket_disable = True

timeout = 120
