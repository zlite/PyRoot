import sys
import threading

# Constants:
priorityLower = -1


# This class is just a specification of what an Event must have in order
# to work with the EventsManager:
class Event(object):
    def __init__(self):
        # These must be defined by the user:
        self.source = None  # Object (instance) that originates the event.
        self.condition = None  # Condition to be used by the test function.
        self.testFunction = None  # Function to be used to evaluate the data.
        self.task = None  # Function to be ran if the event is triggered.
        self.stop = None  # Function to be ran if the event is stopped.


class EventThread(threading.Thread):
    def __init__(self, eventsManager, task, data):
        threading.Thread.__init__(self)
        self.eventsManager = eventsManager
        self.task = task
        self.data = data
        self._stopped = False

    @property
    def running(self):
        return not self._stopped

    def run(self):
        try:
            self.task(self.data)
        except ValueError as error:
            # print error.args[0]  # ##Debug.
            pass
        finally:
            # This flag is critical: it makes the current thread to return
            # without setting the _currentEventIndex to the idlePriority,
            # since if _stopped is True, that means that the process was
            # interrupted by a higher priority event, and so Arbitrate will
            # assign the priority itself.
            if self._stopped:
                self._stopped = False
                return
            #print "-----thread unlocked----"  # ##Debug.
            self.eventsManager._currentEventIndex = self.eventsManager.idlePriority()

    def stop(self):
        self._stopped = True


class EventsManager(object):
    def __init__(self):
        self._running = False

        self._idleEvent = Event()
        self._idleEvent.source = self
        self._idleEvent.condition = None
        self._idleEvent.testFunction = self._idleEventTest
        self._idleEvent.task = self._idleEventDummyTask
        self._idleEvent.stop = self._idleEventDummyStop

        self._events = [self._idleEvent]
        # print self._events  # ##Debug.

    @property
    def running(self):
        return self._running

    def _idleEventTest(self, data, event):
        return True

    def _idleEventDummyTask(self, data):
        pass

    def _idleEventDummyStop(self):
        pass

    def _runEvent(self, event, data):
        self._currentEventThread = EventThread(self, event.task, data)
        self._currentEventThread.start()

    def _stopEvent(self, event):
        self._currentEventThread.stop()
        event.stop()

    def idlePriority(self):
        return len(self._events) - 1

    def start(self):
        self._currentEventIndex = self.idlePriority()
        self._running = True

        # Creates a dummy idle event:
        self._currentEventThread = EventThread(
            self, self._idleEvent.task, None
        )
        self._currentEventThread.start()

        # Tries to arbitrate the start event, which may not necessarily exist:
        self.arbitrate(self, None)

    def stop(self):
        self._running = False
        # This is inside a try-except block because stop is often called
        # without the events system initialized. And using a try-except is
        # safer and more straightforward than keeping track of the system's
        # initialization, etc.
        try:
            self._stopEvent(self._events[self._currentEventIndex])
        except:
            # print "EventsManager.stop error:", sys.exc_info()[0]  # ##Log.
            pass  # ##Future: Log using the data on the previous line.

    # The idle event is always there, and that's a precondition for
    # the insert to work propperly:
    def insert(self, priority, event):
        if priority == priorityLower:
            self._events.insert(len(self._events) - 1, event)
            return

        if priority < priorityLower:
            priority = 0

        # As l.insert(len(l), item) is the same as l.append(item), only checks
        # for not to inserting after the idle event:
        if priority >= len(self._events):
            priority = len(self._events) - 1
        self._events.insert(priority, event)

    def remove(self, priority):
        ##Implement.
        pass

    def removeAll(self, priority):
        ##Implement.
        pass

    def list(self):
        result = []
        for i in self._events:
            result.append(i)
        return result

    def arbitrate(self, source, data, brakePriority=False):
        if not self.running:
            return

        if brakePriority:
            events = self._events[:]
        else:
            # Evaluates only the events with higher priority than the current:
            events = self._events[0: self._currentEventIndex]

        # print ""  # ##Debug.
        # print self._currentEventIndex, ":", events  # ##Debug.
        for i in events:
            # Evaluates only events belonging to the specified source:
            if i.source == source:
                if i.testFunction(data, i):
                    self._stopEvent(self._events[self._currentEventIndex])
                    self._currentEventIndex = self._events.index(i)
                    # ##Debug:
                    # print "New event triggered:", self._currentEventIndex
                    self._runEvent(i, data)
                    break
