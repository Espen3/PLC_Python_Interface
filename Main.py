from pycomm3 import logix_driver
from plc_connect import connect, modchange
from plc_get_tags  import get_tags
from plc_snapshot  import snapshot
from plc_watch     import watch
from plc_write     import write
from plc_monitor   import monitor
from plc_structure import structure

PLC_IP ='192.168.10.200'

def main():
    while True:
        print("\n=== PLC Toolkit ===")
        print("1. Connect / controller info")
        print("2. Get tag list")
        print("3. Take baseline snapshot")
        print("4. Watch a tag")
        print("5. Write to a tag")
        print("6. Live monitor")
        print("7. Controller structure")
        print("8. Change PLC mode (v 1.0)")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            connect(PLC_IP)

        elif choice == '2':
            get_tags(PLC_IP)

        elif choice == '3':
            snapshot(PLC_IP)

        elif choice == '4':
            tag = input("Tag name to watch: ").strip()
            duration = input("Duration in seconds (default 15): ").strip()
            duration = int(duration) if duration.isdigit() else 15
            watch(PLC_IP, tag, duration)

        elif choice == '5':
            tag = input("Tag name to write: ").strip()
            value = input("Value to write: ").strip()
            # Convert to correct type automatically
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            elif '.' in value:
                value = float(value)
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass  # leave as string
            write(PLC_IP, tag, value)

        elif choice == '6':
            tags_input = input("Tags to monitor (comma separated): ").strip()
            tags = [t.strip() for t in tags_input.split(',')]
            interval = input("Poll interval in seconds (default 1): ").strip()
            interval = int(interval) if interval.isdigit() else 1
            monitor(PLC_IP, tags, interval)

        elif choice == '7':
            structure(PLC_IP)

        elif choice == '8':
            modchange(PLC_IP)

        elif choice == '0':
            print("Exiting.")
            break

        else:
            print("Invalid option — try again")

if __name__ == '__main__':
    main()
