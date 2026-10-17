import unittest
from PIL import Image,ImageDraw
from map27_pixel_derivative import derive_map_image,validate_map_image

class Map27PixelDerivative(unittest.TestCase):
    def test_1536_source_is_preserved_and_export_grid_alpha_are_valid(self):
        im=Image.new('RGBA',(1024,1536));ImageDraw.Draw(im).rectangle((200,100,800,1500),fill=(111,77,33,255));original=im.tobytes()
        out,meta=derive_map_image(im);validate_map_image(out)
        self.assertEqual(out.size,(512,768));self.assertEqual(meta['source_to_export'],[.5,.5]);self.assertEqual(im.tobytes(),original)
        self.assertEqual(out.getpixel((0,0))[3],0)
        out.putpixel((100,100),(1,2,3,255))
        with self.assertRaises(ValueError):validate_map_image(out)
    def test_opaque_or_empty_source_rejected(self):
        for im in [Image.new('RGBA',(10,10),'white'),Image.new('RGBA',(10,10))]:
            with self.assertRaises(ValueError):derive_map_image(im)

if __name__=='__main__':unittest.main()
