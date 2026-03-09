import re
import sys
import argparse
import html

# --- KONFIGURACJA WIZUALNA ---
MARGIN = 150        # Margines dookoła całego drzewa
NODE_RADIUS = 35    # Promień koła węzła
FONT_SIZE = 16      # Rozmiar czcionki
TEXT_OFFSET = 60    # Jak nisko pod środkiem koła ma być tekst

class TreeNode:
    def __init__(self, name):
        # Ucieczka znaków specjalnych dla XML (np. <EOF>)
        self.name = html.escape(name)
        self.children = []
        self.x = 0
        self.y = 0

def parse_antlr_tree(tree_str):
    tokens = re.findall(r'\(|\)|"[^"]*"|[^\s()]+', tree_str)
    stack = []
    root = None

    for token in tokens:
        if token == '(':
            stack.append(None)
        elif token == ')':
            child = stack.pop()
            if stack:
                if stack[-1] is None:
                    stack[-1] = child
                else:
                    stack[-1].children.append(child)
            else:
                root = child
        else:
            node = TreeNode(token.strip('"'))
            if stack and stack[-1] is None:
                stack[-1] = node
            elif stack:
                stack[-1].children.append(node)
            else:
                root = node
    return root

def layout_tree(node, depth=0, x_offset=0, x_spacing=200, y_spacing=150):
    # Dodajemy MARGIN do y, aby góra nie była przycięta
    node.y = depth * y_spacing + MARGIN
    
    if not node.children:
        node.x = x_offset + MARGIN
        return x_offset + x_spacing

    current_x = x_offset
    child_centers = []
    
    for child in node.children:
        next_x = layout_tree(child, depth + 1, current_x, x_spacing, y_spacing)
        child_centers.append(child.x)
        current_x = next_x
    
    node.x = (child_centers[0] + child_centers[-1]) / 2
    return current_x

def generate_svg_elements(node, lines, nodes):
    for child in node.children:
        lines.append(f'<line x1="{node.x}" y1="{node.y}" x2="{child.x}" y2="{child.y}" stroke="#A0A0A0" stroke-width="2" />')
        generate_svg_elements(child, lines, nodes)
    
    color = "#3498db" if node.children else "#2ecc71"
    nodes.append(
        f'<g transform="translate({node.x},{node.y})">'
        f'<circle r="{NODE_RADIUS}" fill="{color}" stroke="#2980b9" stroke-width="3" />'
        f'<text y="{TEXT_OFFSET}" font-family="Verdana" font-size="{FONT_SIZE}" font-weight="bold" text-anchor="middle" fill="#2c3e50">{node.name}</text>'
        f'</g>'
    )

def main():
    parser = argparse.ArgumentParser(description="Konwerter drzewa ANTLR do formatu SVG z bezpiecznymi marginesami.")
    parser.add_argument("input", help="Ścieżka do pliku wejściowego (tekst)")
    parser.add_argument("output", help="Ścieżka do pliku wyjściowego (.svg)")
    parser.add_argument("--x_space", type=int, default=220, help="Odstęp poziomy")
    parser.add_argument("--y_space", type=int, default=180, help="Odstęp pionowy")
    
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            tree_data = f.read()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {args.input}")
        sys.exit(1)

    root = parse_antlr_tree(tree_data)
    if not root:
        print("Błąd: Drzewo jest puste lub niepoprawne.")
        sys.exit(1)

    # Obliczanie pozycji (z uwzględnieniem marginesu wewnątrz funkcji)
    max_x_offset = layout_tree(root, x_spacing=args.x_space, y_spacing=args.y_space)
    
    lines = []
    nodes = []
    generate_svg_elements(root, lines, nodes)

    # Szukanie ekstremów, aby dopasować płótno
    all_x = []
    all_y = []
    def collect_coords(n):
        all_x.append(n.x)
        all_y.append(n.y)
        for c in n.children: collect_coords(c)
    collect_coords(root)

    # Rozmiar płótna: Max koordynaty + margines bezpieczeństwa na promienie i tekst
    canvas_width = max(all_x) + MARGIN
    canvas_height = max(all_y) + MARGIN + TEXT_OFFSET

    svg_header = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        f'<svg width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" '
        f'xmlns="http://www.w3.org/2000/svg">\n'
        f'<rect width="100%" height="100%" fill="#ffffff" />\n'
    )
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_header)
        f.write("\n".join(lines))
        f.write("\n")
        f.write("\n".join(nodes))
        f.write("\n</svg>")


if __name__ == "__main__":
    main()