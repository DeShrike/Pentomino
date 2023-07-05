BLACK = "000000"
RED = "FF0000"
GREEN = "00FF00"
YELLOW = "FFFF00"
BLUE = "0000FF"
MAGENTA = "FF00FF"
CYAN = "00FFFF"
WHITE = "FFFFFF"

def to_color_class(color: str, fillcolor: str = None) -> str:
    sc = "str0"
    if color == BLACK:
        sc = "strblack"
    elif color == RED:
        sc = "strred"
    elif color == GREEN:
        sc = "strgreen"
    elif color == YELLOW:
        sc = "stryellow"
    elif color == BLUE:
        sc = "strblue"
    elif color == MAGENTA:
        sc = "strmagenta"
    elif color == CYAN:
        sc = "strcyan"
    elif color == WHITE:
        sc = "strwhite"

    fc = "fil0"
    if fillcolor == BLACK:
        fc = "filblack"
    elif fillcolor == RED:
        fc = "filred"
    elif fillcolor == GREEN:
        fc = "filgreen"
    elif fillcolor == YELLOW:
        fc = "filyellow"
    elif fillcolor == BLUE:
        fc = "filblue"
    elif fillcolor == MAGENTA:
        fc = "filmagenta"
    elif fillcolor == CYAN:
        fc = "filcyan"
    elif fillcolor == WHITE:
        fc = "filwhite"

    return fc + " " + sc           

SVG_START = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="{{PAPERWIDTH}}mm"
   height="{{PAPERHEIGHT}}mm"
   viewBox="0 0 {{PAPERWIDTH}} {{PAPERHEIGHT}}"
   version="1.1"
   id="{{ID}}"
   inkscape:version="1.0.2 (e86c870, 2021-01-15)"
   sodipodi:docname="{{FILENAME}}">

   <defs>
      <style type="text/css">
      <![CDATA[
      .strblack   {stroke:black;  stroke-width:0.0762;stroke-miterlimit:4}
      .strred     {stroke:red;    stroke-width:0.0762;stroke-miterlimit:4}
      .strgreen   {stroke:lime;   stroke-width:0.0762;stroke-miterlimit:4}
      .stryellow  {stroke:yellow; stroke-width:0.0762;stroke-miterlimit:4}
      .strblue    {stroke:blue;   stroke-width:0.0762;stroke-miterlimit:4}
      .strmagenta {stroke:fuchsia;stroke-width:0.0762;stroke-miterlimit:4}
      .strcyan    {stroke:aqua;   stroke-width:0.0762;stroke-miterlimit:4}
      .strwhite   {stroke:white;  stroke-width:0.0762;stroke-miterlimit:4}
      .fil0       {fill:none}
      .str0       {stroke:none}
      .filblack   {fill:black}
      .filred     {fill:red}
      .filgreen   {fill:lime}
      .filyellow  {fill:yellow}
      .filblue    {fill:blue}
      .filmagenta {fill:fuchsia}
      .filcyan    {fill:aqua}
      .filwhite   {fill:white}
      .textstyle  {font-style:normal;font-weight:normal;line-height:1;font-family:sans-serif;}

      ]]>
   </style>
   </defs>
   
   <sodipodi:namedview
      id="base"
      pagecolor="#ffffff"
      bordercolor="#666666"
      borderopacity="1.0"
      inkscape:pageopacity="0.0"
      inkscape:pageshadow="2"
      inkscape:zoom="0.5"
      inkscape:cx="236.8621"
      inkscape:cy="759.4905"
      inkscape:document-units="mm"
      inkscape:current-layer="layer1"
      inkscape:document-rotation="0"
      showgrid="false"
      inkscape:window-width="1267"
      inkscape:window-height="1040"
      inkscape:window-x="629"
      inkscape:window-y="0"
      inkscape:window-maximized="0" />
   <metadata
      id="metadata5">
      <rdf:RDF>
         <cc:Work rdf:about="">
            <dc:format>image/svg+xml</dc:format>
            <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
            <dc:title />
         </cc:Work>
      </rdf:RDF>
   </metadata>
"""

SVG_END = "</svg>"

GROUP_START = """
   <g id="group_{{ID}}">
"""

GROUP_END = "</g>"

LAYER_START = """<g
   inkscape:label="{{NAME}}"
   inkscape:groupmode="layer"
   id="layer_{{ID}}">
"""

LAYER_END = "</g>"

PATH_XML = """
   <path
      id="{{ID}}"
      class="{{COLORCLASS}}"
      x-fill="none" x-stroke="#{{COLOR}}"
      d="{{DATA}}"
      sodipodi:nodetypes="{{NODETYPES}}" />
"""

TEXT_XML = """
   <text xml:space="preserve"
      class="{{COLORCLASS}} textstyle"
      style="font-size:{{FONTSIZE}}px"
      x="{{X}}" y="{{Y}}"
      x-stroke="#{{COLOR}}" x-fill="#{{FILLCOLOR}}"
      id="{{ID}}" {{TRANSFORM}}><tspan
         class="{{COLORCLASS}}"
         sodipodi:role="line"
         id="{{ID}}"
         x="{{X}}"
         y="{{Y}}"
         x-style="stroke-width:7.62">{{TEXT}}</tspan></text>
"""

ELLIPSE_XML = """
   <ellipse
      class="{{COLORCLASS}}"
      x-fill="#{{FILLCOLOR}}" x-stroke="#{{COLOR}}"
      id="{{ID}}"
      cx="{{X}}"
      cy="{{Y}}"
      rx="{{RX}}"
      ry="{{RY}}" />
"""
