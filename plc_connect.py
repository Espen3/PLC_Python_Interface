from pycomm3 import LogixDriver

def connect(plc_ip):
    with LogixDriver(plc_ip) as plc:
        print("Connected successfully")
        print("Controller name:    ", plc.info['name'])
        print("Serial number:      ", plc.info['serial'])
        print("Firmware revision:  ", plc.info['revision'])
        #print("Current mode:       ", plc.info['controller_mode'])
        print("Keyswitch position: ", plc.info['keyswitch'])

    with LogixDriver(plc_ip) as plc:
        info = plc.info
        print("All fields returned by plc.info:\n")
        for key, value in info.items():
            print(f" {key}: {value}")

    meths = [m for m in dir(LogixDriver) if not m.startswith('_')]
    for m in meths:
        print(m)
        
def modchange(plc_ip):
    mode_choice = input("Select PLC mode Run or Prog (else exit): ")
    with LogixDriver(plc_ip) as plc:
        while True:
            if mode_choice == 'Run':
                plc.change_to_running()
                print("Changing mode to Running")
                break

            if mode_choice == 'Prog':
                plc.change_to_program()
                print("Changing mode to Programming")
                break

            else:
                print("Invalid choice. Exiting to menu")
                break
