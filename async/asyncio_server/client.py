import asyncio
import datetime
import random

from measurement_pb2 import MeasurementRecord, RequestMessage, ResponseMessage
import constants as C
from enums import PersonName

people = [person.value for person in list(PersonName)]

def get_random_message() -> RequestMessage:
    array_size = 1
    num_records = 2
    reqm = RequestMessage()
    record = MeasurementRecord()
    record.id = random.randint(1,100000)
    record.measurerName = random.choice(people)
    record.download.extend([random.random() for i in range(array_size)])
    record.upload.extend([random.random() for i in range(array_size)])
    record.ping.extend([random.random() for i in range(array_size)])
    record.timestamp = int(datetime.datetime.now().timestamp())
    reqm.measurement_records.extend([record] * num_records)
    return reqm

async def run_single_client(req_count: int, address: str, port: int):
    reader, writer = await asyncio.open_connection(address, port)
    for req in range(req_count):
        message = get_random_message()
        serialized_message = message.SerializeToString()
        writer.write(serialized_message + C.END_OF_MESSAGE)
        await writer.drain()
        print("Wrote message {} to client".format(req))
        data: bytes = await reader.readuntil(separator=C.END_OF_MESSAGE)
        received_message = ResponseMessage()
        received_message.ParseFromString(data[:-1])
        print("Received {} calculated records".format(len(received_message.measurement_averages)))
    print('Closing the connection..')
    writer.close()
    await writer.wait_closed()
async def test_client_heavy_traffic():
    clients = 1
    req_count = 10
    address = "127.0.0.1"
    port = 12345
    x = await asyncio.gather(*(run_single_client(req_count, address, port) for cl in range(clients)))

if __name__ == '__main__':
    asyncio.run(test_client_heavy_traffic())