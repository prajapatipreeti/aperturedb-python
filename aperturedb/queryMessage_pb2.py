# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: queryMessage.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='queryMessage.proto',
  package='VDMS.protobufs',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12queryMessage.proto\x12\x0eVDMS.protobufs\":\n\x0cqueryMessage\x12\x0c\n\x04json\x18\x01 \x01(\t\x12\r\n\x05\x62lobs\x18\x02 \x03(\x0c\x12\r\n\x05token\x18\x03 \x01(\tb\x06proto3')
)




_QUERYMESSAGE = _descriptor.Descriptor(
  name='queryMessage',
  full_name='VDMS.protobufs.queryMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='json', full_name='VDMS.protobufs.queryMessage.json', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blobs', full_name='VDMS.protobufs.queryMessage.blobs', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='token', full_name='VDMS.protobufs.queryMessage.token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=96,
)

DESCRIPTOR.message_types_by_name['queryMessage'] = _QUERYMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

queryMessage = _reflection.GeneratedProtocolMessageType('queryMessage', (_message.Message,), {
  'DESCRIPTOR' : _QUERYMESSAGE,
  '__module__' : 'queryMessage_pb2'
  # @@protoc_insertion_point(class_scope:VDMS.protobufs.queryMessage)
  })
_sym_db.RegisterMessage(queryMessage)


# @@protoc_insertion_point(module_scope)
