import json
from sflow import Trace

def write_file(dict):
    with open('output.json', 'a') as file:
        json.dump(dict, file, sort_keys=True, indent=4)

if __name__ == '__main__':

    myTrace = Trace(callable=write_file)

    with open('./data/SFLOW2.log') as f:
        for line in f:
            myTrace.process(line)

