from pycomm3 import LogixDriver
import time
import os

def monitor(plc_ip, tags, poll_interval=1):
    with LogixDriver(plc_ip) as plc:
        print(f"Connected: {plc.info['name']}")
        print(f"Monitoring {len(tags)} tags — Ctrl+C to stop\n")

        previous = {}

        while True:
            try:
                results = plc.read(*tags)
                if not isinstance(results, list):
                    results = [results]

                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"=== PLC Monitor — {plc.info['name']} ===\n")

                for r in results:
                    if r.error:
                        print(f"  {r.tag:<35} ERROR: {r.error}")
                        continue
                    changed = r.tag in previous and previous[r.tag] != r.value
                    marker = " <-- CHANGED" if changed else ""
                    print(f"  {r.tag:<35} {str(r.value):<20} {r.type}{marker}")
                    previous[r.tag] = r.value

                time.sleep(poll_interval)

            except KeyboardInterrupt:
                print("\nMonitor stopped.")
                break