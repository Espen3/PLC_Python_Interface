from pycomm3 import LogixDriver
import json
from datetime import datetime

PLC_IP = '192.168.1.10'
SIMPLE_TYPES = {'BOOL', 'DINT', 'INT', 'SINT', 'LINT', 'REAL', 'STRING'}


def read_tags_in_batches(plc, tag_names, batch_size=20):
    """Read a list of tags in batches, return dict of name:value"""
    results = {}
    for i in range(0, len(tag_names), batch_size):
        batch = tag_names[i:i + batch_size]
        response = plc.read(*batch)
        if not isinstance(response, list):
            response = [response]
        for r in response:
            if r.error:
                results[r.tag] = {'value': 'READ_ERROR', 'error': r.error}
            else:
                results[r.tag] = {'value': r.value, 'type': r.type}
    return results


with LogixDriver(PLC_IP) as plc:
    print("Connected:", plc.info['name'])
    programs = plc.info.get('programs', {})

    full_dump = {
        'timestamp': datetime.now().isoformat(),
        'controller': plc.info['name'],
        'controller_tags': {},
        'programs': {}
    }

    # --- Controller-scoped tags ---
    print("Reading controller tags...")
    ctrl_tags = plc.get_tag_list()
    ctrl_simple = [t['tag_name'] for t in ctrl_tags if t['data_type'] in SIMPLE_TYPES]
    full_dump['controller_tags'] = read_tags_in_batches(plc, ctrl_simple)
    print(f"  {len(ctrl_simple)} tags read")

    # --- Program-scoped tags ---
    for prog in programs:
        print(f"Reading program: {prog}...")
        prog_tags = plc.get_tag_list(f'Program:{prog}')
        prog_simple = [t['tag_name'] for t in prog_tags if t['data_type'] in SIMPLE_TYPES]

        # Must prefix with Program:Name. to read program-scoped tags
        prefixed = [f'Program:{prog}.{t}' for t in prog_simple]
        raw_results = read_tags_in_batches(plc, prefixed)

        # Strip the prefix back off for cleaner output
        clean_results = {
            k.replace(f'Program:{prog}.', ''): v
            for k, v in raw_results.items()
        }

        full_dump['programs'][prog] = clean_results
        print(f"  {len(prog_simple)} tags read")

    # Save
    with open('plc_full_dump.json', 'w') as f:
        json.dump(full_dump, f, indent=2, default=str)

    print(f"\nFull dump saved to plc_full_dump.json")