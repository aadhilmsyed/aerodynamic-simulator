import pandas as pd
from pathlib import Path
import re

def clean_column_name(name):
    """Convert column names to LaTeX-friendly format"""
    name = name.replace('_', ' ').title()
    # Handle special cases
    name = name.replace('Lift To Drag', 'L/D Ratio')
    return name

def csv_to_latex(csv_path, output_dir):
    """Convert a CSV file to a LaTeX table"""
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Get flap type from filename
    flap_type = csv_path.stem.replace('_', ' ').title()
    
    # Create LaTeX table content
    latex_content = [
        "\\begin{table}[h!]",
        "\\centering",
        "\\caption{Aerodynamic Data for " + flap_type + "}",
        "\\label{tab:" + csv_path.stem + "}",
        "\\begin{tabular}{" + "c" * len(df.columns) + "}",
        "\\hline"
    ]
    
    # Add headers
    headers = [clean_column_name(col) for col in df.columns]
    latex_content.append(" & ".join(headers) + " \\\\")
    latex_content.append("\\hline")
    
    # Add data rows
    for _, row in df.iterrows():
        formatted_row = [f"{x:.3f}" if isinstance(x, float) else str(x) for x in row]
        latex_content.append(" & ".join(formatted_row) + " \\\\")
    
    # Close table
    latex_content.extend([
        "\\hline",
        "\\end{tabular}",
        "\\end{table}"
    ])
    
    # Write to file
    output_path = output_dir / f"{csv_path.stem}_table.tex"
    with open(output_path, 'w') as f:
        f.write('\n'.join(latex_content))

def main():
    # Create output directory
    output_dir = Path("output/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all CSV files in the data directory
    data_dir = Path("output/data")
    if data_dir.exists():
        for csv_file in data_dir.glob("*.csv"):
            csv_to_latex(csv_file, output_dir)
            print(f"Generated LaTeX table for {csv_file.name}")
    else:
        print("No data directory found. Please run the simulator first to generate CSV files.")

if __name__ == "__main__":
    main() 