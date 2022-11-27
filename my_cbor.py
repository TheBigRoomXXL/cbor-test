import json
from pprint import pprint
from cbor2 import CBORTag, dumps, loads
from cbor2.tool import key_to_str

class Detection:
  def __init__(self, timer, event, bib, timestamp):
    self.timer = timer
    self.event = event
    self.bib = bib
    self.timestamp = timestamp
  
  @staticmethod
  def from_bytes(msg : bytes)-> list[Detection]:
    timer = tag.value[0:2]
    event = tag.value[2:4]
    data = tag.value[4:]
    for item in data:
      detection = Detection(
        timer=timer, 
        event=event, 
        bib=item[0], 
        timestamp=item[1]
      )
      yield detection

  

def custom_encoding(encoder, value):
  encoder.encode(CBORTag(6, [value.x, value.y]))

def custom_decoding(decoder, tag, shareable_index=None):
  if tag.tag == 6:
    return Detection.from_bytes(tag.value)
  
  return tag


def cbor_dumps(obj, **kwargs):
  return dumps(obj, datetime_as_timestamp=True, default=custom_encoding, **kwargs)


def cbor_loads(obj, **kwargs):
  return loads(obj, tag_hook=custom_decoding, **kwargs)




if __name__ == '__main__':
  point = Point(10,20)
  z = Detection()
  x = cbor_dumps(z)
  print(x.hex())
  y = cbor_loads(x)
  print(y)
