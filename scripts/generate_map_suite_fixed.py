"""Robust entry point for the portfolio map-suite generator."""
from io import BytesIO
from pathlib import Path
import base64
import importlib.util
import re
import xml.etree.ElementTree as ET

from PIL import Image

# Load the existing generator directly from its file path so this script works
# when executed as `python scripts/generate_map_suite_fixed.py` in Actions.
spec = importlib.util.spec_from_file_location(
    'generate_map_suite', Path('scripts/generate_map_suite.py')
)
maps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maps)


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
