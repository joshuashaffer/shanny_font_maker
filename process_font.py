from xml.etree import ElementTree
import PIL.Image
import numpy


def vec2int(line):
    powers = [1 << x if x < 5 else 0 for x in xrange(len(line))]
    l = 59 + numpy.sum(numpy.array(powers) * numpy.array(line))
    return l


def fontToButte(stinkie_dict, image, image_xml):
    font_image = PIL.Image.open(image)
    document = ElementTree.parse(image_xml)
    font = document.getroot()
    font_data = numpy.array(font_image)[:, :, 3]
    for character in font.getchildren():
        bbox = map(int, character.get('rect').split(' '))
        glyph = character.get('code').encode('utf-8').strip()
        #if bbox[2] > 5:
        #    continue
        if bbox[2] == 0:
            continue
        if glyph in stinkie_dict:
            continue
        # print "{} {}".format(glyph, bbox)
        glyph_raw = numpy.sign(font_data[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]).tolist()
        stinkie_dict[glyph] = ''.join(map(chr, map(vec2int, glyph_raw)))


stinkie_dict = dict()
fontToButte(stinkie_dict, "5x5_regular_5.PNG", "5x5_regular_5.xml")
fontToButte(stinkie_dict, "microsoft_mhei_bold_5.PNG", "microsoft_mhei_bold_5.xml")
fontToButte(stinkie_dict, "microsoft_mhei_bold_4.PNG", "microsoft_mhei_bold_4.xml")
fontToButte(stinkie_dict, "microsoft_mhei_regular_4.PNG", "microsoft_mhei_regular_4.xml")
fontToButte(stinkie_dict, "microsoft_mhei_regular_3.PNG", "microsoft_mhei_regular_3.xml")

for glyph in stinkie_dict.iterkeys():
    print "set ::alphabet({}) \"{}\"".format(glyph, stinkie_dict[glyph])
