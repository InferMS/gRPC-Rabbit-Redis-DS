# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sensorLoadBalancer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18sensorLoadBalancer.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x83\x01\n\x0fSensorMeteoData\x12\n\n\x02id\x18\x01 \x01(\x05\x1a\x64\n\x0cRawMeteoData\x12\x13\n\x0btemperature\x18\x01 \x01(\x02\x12\x10\n\x08humidity\x18\x02 \x01(\x02\x12-\n\ttimestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"q\n\x13SensorPollutionData\x12\n\n\x02id\x18\x01 \x01(\x05\x1aN\n\x10RawPollutionData\x12\x0b\n\x03\x63o2\x18\x01 \x01(\x02\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2\x90\x01\n\x0cLoadBalancer\x12;\n\rsendMeteoData\x12\x10.SensorMeteoData\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\x11sendPollutionData\x12\x14.SensorPollutionData\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sensorLoadBalancer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SENSORMETEODATA._serialized_start=91
  _SENSORMETEODATA._serialized_end=222
  _SENSORMETEODATA_RAWMETEODATA._serialized_start=122
  _SENSORMETEODATA_RAWMETEODATA._serialized_end=222
  _SENSORPOLLUTIONDATA._serialized_start=224
  _SENSORPOLLUTIONDATA._serialized_end=337
  _SENSORPOLLUTIONDATA_RAWPOLLUTIONDATA._serialized_start=259
  _SENSORPOLLUTIONDATA_RAWPOLLUTIONDATA._serialized_end=337
  _LOADBALANCER._serialized_start=340
  _LOADBALANCER._serialized_end=484
# @@protoc_insertion_point(module_scope)
