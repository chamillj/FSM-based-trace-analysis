#@@---------------------------@@
#  Author: Chamil Jayasundara
#  Date: 5/18/17
#  Description:
#@@---------------------------@@

import itertools
from collections import defaultdict

class Container(object):
    # Parent class for trace and flow sample objects

    def __init__(self, id):
        self.id = id
        self.content = defaultdict(int)

    def __getitem__(self, key):
        return self.content[key]

    def __setitem__(self, key, value):
        self.content[key] = value

    def _store(self, line):
        partition = line.partition(" ")
        self.content[partition[0]] = partition[2].rstrip()


class Datagram(Container):

    # Class for the Datagram object

    datagram_counter = itertools.count().next

    def __init__(self):
        super(Datagram, self).__init__(Datagram.datagram_counter(), )
        self['flowSamples'] = {}


class FlowSample(Container):

    # Class for the flow sample object

    flowsample_counter = itertools.count().next

    def __init__(self):
        super(FlowSample, self).__init__(FlowSample.flowsample_counter())


###State Machine Classses

class WithinDatagram(object):
    # State class for the state within datagram

    def __init__(self, traceObj):
        self.Trace = traceObj
        self.current_datagram = None

    def process(self,line):
        if "startDatagram" in line:
            self.current_datagram = Datagram()

        elif "endDatagram" in line:
            self.Trace.callable(self.current_datagram.content)

        elif "startSample" in line:
            self.Trace.currentState = self.Trace.within_flowsample
            self.Trace.within_flowsample.re_init(FlowSample(), self.current_datagram)

        else:
            self.current_datagram._store(line)


class WithinFlowsample(object):

    # state class for the state within flow sample

    def __init__(self, traceObj):
        self.Trace = traceObj
        self.current_datagram = None
        self.current_flowsample = None

    def re_init(self, flowsampleObj, datagramObj):
        self.current_datagram = datagramObj
        self.current_flowsample = flowsampleObj

    def process(self,line):
        if "endSample" in line:
            self.current_datagram['flowSamples'][self.current_flowsample.id] = self.current_flowsample.content
            self.Trace.currentState = self.Trace.within_datagram

        else:
            self.current_flowsample._store(line)


class Trace(object):

    def __init__(self, callable=None):
        # set initial state, i.e within datagram
        self.within_datagram = WithinDatagram(self)
        self.within_flowsample = WithinFlowsample(self)
        self.currentState = self.within_datagram
        self.callable = callable

    def process(self, line):
        self.currentState.process(line)



