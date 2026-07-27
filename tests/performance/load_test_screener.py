import threading
import time
import requests

URL = "http://127.0.0.1:8000/api/v1/screener?min_roe=15"

times = []


def hit_api(index):
    start = time.perf_counter()

    response = requests.get(URL)

    end = time.perf_counter()

    elapsed = end - start

    print(f"Thread {index+1}: {response.status_code} ({elapsed:.3f}s)")

    times.append(elapsed)


threads = []

overall_start = time.perf_counter()

for i in range(10):
    t = threading.Thread(target=hit_api, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

overall_end = time.perf_counter()

print("\n========== SUMMARY ==========")
print(f"Total Time : {overall_end-overall_start:.3f} sec")
print(f"Average    : {sum(times)/len(times):.3f} sec")
print(f"Fastest    : {min(times):.3f} sec")
print(f"Slowest    : {max(times):.3f} sec")