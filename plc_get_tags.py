from pycomm3 import LogixDriver
import json

def get_tags(plc_ip):
    with LogixDriver(plc_ip) as plc:
        print("Connected to:", plc.info['name'])
        print("Pulling tag list...\n")

        controller_tags = plc.get_tag_list()
        programs = plc.info.get('programs', {})

        program_tags = {}
        for prog in programs:
            print(f"Pulling tags for: {prog}")
            program_tags[prog] = plc.get_tag_list(f'Program:{prog}')

        output = {
            'controller_tags': [
                {'name': t['tag_name'], 'type': t['data_type']}
                for t in controller_tags
            ],
            'program_tags': {
                prog: [
                    {'name': t['tag_name'], 'type': t['data_type']}
                    for t in tags
                ]
                for prog, tags in program_tags.items()
            }
        }

        with open('plc_tags.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)

        print(f"\nDone — {len(controller_tags)} controller tags saved to plc_tags.json")