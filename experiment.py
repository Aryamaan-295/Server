import random
import datetime
import uuid



_DATA_KEYS = ["a","b","c"]

class Device:
    def __init__(self, id):
        self._id = id
        self.records = []
        self.sent = []


    def obtainData(self) -> dict:
        """Returns a single new datapoint from the device.
Identified by type `record`. `timestamp` records when the record was sent and `dev_id` is the device id.
        `data` is the data collected by the device."""
        # if random.random() < 0.4:
        #     # Sometimes there's no new data
        #     return {}


        rec = {
            'type': 'record', 'timestamp': datetime.datetime.now().isoformat(), 'dev_id': self._id,
            'data': {kee: str(uuid.uuid4()) for kee in _DATA_KEYS}
        };self.sent.append(rec)
        return rec


    def probe(self) -> dict:
        """Returns a probe request to be sent to the SyncService.
        Identified by type `probe`. `from` is the index number from which the device is asking for the data."""
        # if random.random() < 0.5:
        #     # Sometimes the device forgets to probe the SyncService
        #     return {}


        return {'type': 'probe', 'dev_id': self._id, 'from': len(self.records)}


    def onMessage(self, data: dict):
        """Receives updates from the server"""
        # if random.random() < 0.6:
        #     # Sometimes devices make mistakes. Let's hope the SyncService handles such failures.
        #     return
        
        if data['type'] == 'update':
            _from = data['from']
            if _from > len(self.records):
                return
            self.records = self.records[:_from] + data['data']

class SyncService:
    def __init__(self):
        self.records = []

    def onMessage(self, data: dict):
        """Handle messages received from devices.
        Return the desired information in the correct format (type `update`, see Device.onMessage and testSyncing to understand format intricacies) in response to a `probe`.
        No return value required on handling a `record`."""
        # if data == {}:
        #     print(0)
        #     return {'type': 'update', 'from': 0, 'data': []}
    
        if data['type'] == 'record':
            self.records.append(data)
        
        elif data['type'] == 'probe':
            print(data['from'])
            return {'type': 'update', 'from': data['from'] - 1, 'data': self.records}
        
        else:
            raise NotImplementedError()


dev1 = Device("dev_1")
sync = SyncService()

for i in range(2):
    sync.onMessage(dev1.obtainData())
    dev1.onMessage(sync.onMessage(dev1.probe()))
    print((dev1.records))


# print(len(sync.records))
# print(dev1.probe()['from'])
# print(len(sync.onMessage(dev1.probe())['data']))

# print(dev1.probe()['from'])


# sync.onMessage(dev1.obtainData())

# print(dev1.probe()['from'])


