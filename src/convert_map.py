"""
Script to read a CSV map file and convert symbols to numeric StaticMapState values.
Uses the symbol mapping defined in Map.py.
"""

import csv
import sys
from pathlib import Path

# Inverse symbol map: character -> StaticMapState value
SYMBOL_TO_VALUE = {
    ' ': 0,   # BLANK
    '': 0,    # Empty cell also maps to BLANK
    'S': 1,   # SURVIVOR
    '|': 2,   # WALL_VERTICAL
    '-': 3,   # WALL_HORIZONTAL
    '⊥': 4,   # WALL_T_UP
    'T': 5,   # WALL_T_DOWN
    '├': 6,   # WALL_T_TOP_RIGHT
    '┤': 7,   # WALL_T_TOP_LEFT
    '┐': 8,   # WALL_CORNER_NE
    '┌': 9,   # WALL_CORNER_NW
    '┘': 10,  # WALL_CORNER_SE
    '└': 11,  # WALL_CORNER_SW
    '+': 12,  # WALL_CROSS
}


def convert_cell(cell: str) -> int:
    """
    Convert a single cell value to its numeric StaticMapState value.
    
    Args:
        cell: The cell value from the CSV (can be a symbol or already numeric)
        
    Returns:
        The numeric StaticMapState value
    """
    cell = cell.strip()
    
    # Check if it's already a number
    try:
        return int(cell)
    except ValueError:
        pass
    
    # Look up in symbol map
    if cell in SYMBOL_TO_VALUE:
        return SYMBOL_TO_VALUE[cell]
    
    # Unknown symbol - return as BLANK with warning
    print(f"Warning: Unknown symbol '{cell}', treating as BLANK (0)")
    return 0


def read_and_convert_csv(input_path: str, output_path: str = None):
    """
    Read a CSV map file and convert all symbols to numeric values.
    
    Args:
        input_path: Path to the input CSV file
        output_path: Path to save the converted CSV (if None, prints to stdout)
    """
    converted_rows = []
    
    # Use utf-8-sig to handle BOM (byte order mark) if present
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:  # Skip empty rows
                continue
            converted_row = [convert_cell(cell) for cell in row]
            converted_rows.append(converted_row)
    
    # Output results
    if output_path:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(converted_rows)
        print(f"Converted map saved to: {output_path}")
    else:
        # Print as Python list format for easy copy-paste
        print("Converted map (Python list format):")
        print("[")
        for row in converted_rows:
            print(f"    {row},")
        print("]")
    
    return converted_rows


def main():
    # Default paths
    script_dir = Path(__file__).parent
    default_input = script_dir / "Maps" / "Scenario.csv"
    default_output = script_dir / "Maps" / "Scenario_converted.csv"
    
    # Use command line args if provided
    input_path = sys.argv[1] if len(sys.argv) > 1 else str(default_input)
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(default_output)
    
    print(f"Reading from: {input_path}")
    converted = read_and_convert_csv(input_path, output_path)
    
    print(f"\nMap dimensions: {len(converted)} rows x {len(converted[0]) if converted else 0} cols")
    
    # Also print as Python list for convenience
    print("\nAs Python list (for direct use in code):")
    print("converted_map = [")
    for row in converted:
        print(f"    {row},")
    print("]")


if __name__ == "__main__":
    main()

