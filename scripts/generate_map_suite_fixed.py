"""Robust entry point for the portfolio map-suite generator.

The accepted comparison SVG stores its map image as a data URI. XML parsing is
used here so encoded line breaks/entities in the href are resolved before
base64 decoding.
"""
from io import BytesIO
from pathlib import Path
import base64
import re
import xml.etree.ElementTree as ET

from PIL import Image
import scripts.generate_map_suite as maps


def load_comparison_image():
    svg_path = Path('outputs/maps/final_lulc_comparison.svg')
    root = ET.parse(svg_path).getroot()

    href = None
    for elem in root.iter():
        if elem.tag.rsplit('}', 1)[-1] != 'image':
            continue
        href = (
            elem.attrib.get('href')
            or elem.attrib.get('{http://www.w3.org/1999/xlink}href')
        )
        if href and 'base64,' in href:
            break

    if not href or 'base64,' not in href:
        raise RuntimeError('Embedded comparison image data URI not found')

    data = href.split('base64,', 1)[1]
    data = re.sub(r'\s+', '', data)
    data += '=' * (-len(data) % 4)
    raw = base64.b64decode(data, validate=False)
    return Image.open(BytesIO(raw)).convert('RGB')


maps.load_comparison_image = load_comparison_image

if __name__ == '__main__':
    maps.main()
