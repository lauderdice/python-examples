import asyncio
import datetime
import enum
from typing import Tuple
import constants as C
import numpy as np
import time
import click
import asyncio
from asyncio import StreamReader, StreamWriter, IncompleteReadError
from measurement_pb2 import RequestMessage, MeasurementRecord, ResponseMessage, MeasurementAverage
class DataTransferFormat(enum.Enum):
    JSON = "json"
    Protobuf = "proto"
    Avro = "avro"

class DataProcessor():
    def calculate_averages(self,message: RequestMessage) -> Tuple[ResponseMessage,int]:
        calculated_averages = [self._get_maverage_from_mrecord(x) for x in message.measurement_records]
        resp = ResponseMessage()
        resp.measurement_averages.extend(calculated_averages)
        return resp, len(message.measurement_records)

    def _get_maverage_from_mrecord(self, mrecord: MeasurementRecord) -> MeasurementAverage:
        avg_rec = MeasurementAverage()
        avg_rec.id = mrecord.id
        avg_rec.measurerName = mrecord.measurerName
        avg_rec.download = float(np.mean(mrecord.download))
        avg_rec.upload = float(np.mean(mrecord.upload))
        avg_rec.ping = float(np.mean(mrecord.ping))
        avg_rec.timestamp = mrecord.timestamp
        return avg_rec

class Server():

    def __init__(self, address: str, port: int, format: DataTransferFormat):
        self._address = address
        self._port = port
        self._format = format

    def run(self):
        asyncio.run(self._run_server())


    async def handle_proto_data(self, reader: StreamReader, writer: StreamWriter):
        data_processor = DataProcessor()
        while True:
            try:
                data: bytes = await reader.readuntil(separator=C.END_OF_MESSAGE)
                received_message = RequestMessage()
                received_message.ParseFromString(data[:-1])
                response_message, number_of_records = data_processor.calculate_averages(received_message)
                serialized_response = response_message.SerializeToString()
                writer.write(serialized_response + C.END_OF_MESSAGE)
                await writer.drain()
                print("Calculated averages for {} measurement records".format(number_of_records))
            except IncompleteReadError:
                print("EOF detected. Exiting..")
                break


    async def _handle_connection(self, reader: StreamReader, writer: StreamWriter):
        if self._format == DataTransferFormat.Protobuf:
            await self.handle_proto_data(reader, writer)
        elif self._format == DataTransferFormat.JSON:
            print("Not implemented")
        elif self._format == DataTransferFormat.Avro:
            print("Not implemented")

        print("Closing the connection..")
        writer.close()

    async def _run_server(self):
        server = await asyncio.start_server(
            self._handle_connection, self._address, self._port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print("Serving on {}".format(addrs))
        async with server:
            await server.serve_forever()







@click.command()
@click.option('--dataformat', default="proto", help='json, proto, avro',prompt='Data transfer format can be 3 types: json, proto, avro')
@click.option('--port', default=12345, prompt='Port to run the server on')
@click.option('--address', default="127.0.0.1",prompt='Address to run the server on')
def main(address: str, port: int, dataformat: str):
    s = Server(address, port, DataTransferFormat(dataformat))
    s.run()

if __name__ == '__main__':
    main()



