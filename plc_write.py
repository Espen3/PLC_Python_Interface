from pycomm3 import LogixDriver
import time

def write(plc_ip, tag, value):
    with LogixDriver(plc_ip) as plc:
        before = plc.read(tag)

        if before.error:
            print(f"Cannot read tag — aborting. Error: {before.error}")
            return

        print(f"Tag:           {tag}")
        print(f"Type:          {before.type}")
        print(f"Current value: {before.value}")
        print(f"New value:     {value}")
        print()

        confirm = input("Are you sure you want to write this value? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Aborted — nothing was changed")
            return

        result = plc.write((tag, value))

        if result.error:
            print(f"Write failed: {result.error}")
            return

        time.sleep(2)
        after = plc.read(tag)
        print(f"\nValue after write: {after.value}")

        if str(after.value) == str(value):
            print("SUCCESS — value confirmed")
        else:
            print(f"WARNING — value does not match what we wrote")
            print(f"Expected {value}, got {after.value}")
