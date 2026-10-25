import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from asset_delivery import validate
class DeliveryTest(unittest.TestCase):
 def test_valid_and_rejections(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);Image.new('RGBA',(40,40)).save(folder/'face.png')
   slot=dict(role='face/granny/joy',state='joy',sha256='current',module='대사 얼굴',path='assets/old.png',size=[40,40])
   item=dict(role=slot['role'],state='joy',baseline_sha256='current',file='face.png',size=[40,40])
   with patch('asset_delivery.inventory',return_value=[slot]):
    self.assertTrue(validate(dict(items=[item]),folder)['valid'])
    for bad in [dict(item,baseline_sha256='old'),dict(item,file='../outside.png'),dict(item,size=[2,2]),dict(item,role='unknown')]:
     self.assertFalse(validate(dict(items=[bad]),folder)['valid'])
    self.assertFalse(validate(dict(items=[item,item]),folder)['valid'])
    self.assertFalse(validate(dict(items=[]),folder)['valid'])
if __name__=='__main__':unittest.main()
