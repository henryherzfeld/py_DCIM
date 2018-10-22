from pysnmp.hlapi.asyncio import (
    bulkCmd,
    getCmd,
    CommunityData,
    UdpTransportTarget,
    SnmpEngine,
    ContextData,
    ObjectIdentity,
    ObjectType,

)
from pysnmp.smi import view
import asyncio
import logging
from dcim.configuration import get_config

LOGGER = logging.getLogger(__name__)


# Adaption of PySNMP Engine, performs all SNMP processing asynchronously
class SNMPEngine:
    requests = []
    targets = []
    results = []
    community_string = ''
    timeout = 0
    snmpEngine = 0
    loop = 0
    queue = 0
    mibViewController = 0

    def __init__(self, targets):
        self.requests = []
        self.targets = targets
        self.results = []
        self.community_string = get_config('snmp')['COMM_STRING']
        self.timeout = get_config('snmp')['TIMEOUT']
        self.snmpEngine = SnmpEngine()
        self.mibBuilder = self.snmpEngine.getMibBuilder()
        self.mibViewController = view.MibViewController(self.mibBuilder)
        self.loop = asyncio.get_event_loop()

    # process a single SNMP request asynchronously, requires host and snmp_object
    async def get_snmp_request(self, host, target):

        print("attempting SNMP for " + host)

        response = await getCmd(
            self.snmpEngine,
            CommunityData(self.community_string, mpModel=1),
            UdpTransportTarget((host, 161)),
            ContextData(),
            target,
        )

        error_indication, error_status, error_index, varbinds = response

        if error_indication:
            LOGGER.warning('%s with this asset: %s', error_indication, host)
            return

        elif error_status:
            LOGGER.warning(
                '%s at %s',
                error_status.prettyPrint(),
            )
            return

        else:
            return varbinds.items()

    # retrieves snmp data from each target's equipment, builds and sorts dictionary of lists
    # where key is ip and value is array of all oids, stores request calls for each ip in event loop
    def enqueue_requests(self):
        print('enqueueing requests')

        for target in self.targets:
            for equipment in target.contains:
                for snmp_request in equipment.snmp_requests:

                    # creating redis-ready key:value as label:request to be returned as label:reponse post-snmp
                    self.requests.append({
                        equipment.get_label():

                        self.loop.create_task(
                            self.get_snmp_request(equipment.ip, snmp_request)
                        )
                    })

    def process_requests(self):
        print('processing request queue')

        for request in self.requests:
            for label, request_data in request.items():
                response = self.loop.run_until_complete(request_data)
                print({label: response})
                return {label: response}