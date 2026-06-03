from pycomm3 import LogixDriver
import time

def watch(plc_ip, tag, duration=15):
    print(f"Watching '{tag}' for {duration} seconds...")
    print("Do not touch the process during this time\n")

    values_seen = []

    with LogixDriver(plc_ip) as plc:
        for i in range(duration):
            result = plc.read(tag)
            if result.error:
                print(f"Error reading tag: {result.error}")
                break
            values_seen.append(result.value)
            print(f"  Second {i+1:02d}: {result.value}")
            time.sleep(1)

    unique_values = set(str(v) for v in values_seen)
    print("\n--- Result ---")
    if len(unique_values) > 1:
        print(f"Tag changed on its own: {unique_values}")
        print("DO NOT write to this tag — the PLC is controlling it")
    else:
        print(f"Tag held steady at: {values_seen[0]}")
        print("Tag appears stable — likely safe to write")