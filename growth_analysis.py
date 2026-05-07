import pandas as pd
import string
import matplotlib.pyplot as plt
import numpy as np
import os

def data_table(file_path):
    
    plates_sizes = {
        6 : {'rows': 2, 'cols': 3},
        12 : {'rows': 3, 'cols': 4},
        24 : {'rows': 4, 'cols': 6},
        96 : {'rows': 8, 'cols': 12},
        384 : {'rows': 16, 'cols': 24}
    }

    df = pd.read_csv(file_path, skiprows = 9)
    print(df.head())

    num_cols = len(df.columns) - 2

    detected_plate = None
    for row, col in plates_sizes.items():
        if col['cols'] == num_cols:
            detected_plate = row
            break
    if detected_plate:
        read_this = plates_sizes[detected_plate]['rows']
        print(f'✓ Detected: {detected_plate} well plate — reading {read_this} rows')
        df = pd.read_csv(file_path, skiprows=9, nrows= read_this)
    else:
        print(f'✗ Unknown plate size — {num_cols} columns not in list')

    table_data = df.iloc[0:read_this, 1:num_cols + 1]

    row_labels = [string.ascii_uppercase[i] for i in range(len(table_data))]
    table_data.insert(0, 'Row_Label', row_labels)

    print(table_data)
    return table_data

def heat_map(table_data, threshold, file_path, output_folder):
    pass_wells = []
    fail_wells = []

    fig, ax = plt.subplots(figsize = (20, 10))
    ax.axis('off')

    table = ax.table(cellText = table_data.values, colLabels =table_data.columns, loc = 'center', cellLoc = 'center')
    for (i,j), val in table.get_celld().items():
        if i > 0:
            cell_value = table_data.iloc[i-1, j]
            if isinstance(cell_value, (int, float)):
                if cell_value < threshold:
                    color = 'red'
                    fail_wells.append(f'{table_data.iloc[i-1, 0]}{j}')
                else:
                    color = 'green'
                    pass_wells.append(f'{table_data.iloc[i-1,0]}{j}')
                val.set_facecolor(color)
                val.set_text_props(color = 'white')

    from matplotlib.patches import Patch
    legend_element = [
        Patch(facecolor = 'green', edgecolor = 'black', label = f'Pass > {threshold}'),
        Patch(facecolor = 'red', edgecolor = 'black', label = f'Fail < {threshold}')
    ]
    fig.legend(handles = legend_element, loc = 'upper right', fontsize = 14)

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    file_name = os.path.basename(file_path).replace('.csv', '')
    plt.title(f'Growth Analysis, {file_name}', fontsize = 24)
    plt.show()

    print(f'Passed wells, {pass_wells}')
    print(f'Failed wells, {fail_wells}')

    heatmap_path = os.path.join(output_folder, f'{file_name}_heatmap.png')
    fig.savefig(heatmap_path)
    print(f'✓ Heatmap saved to: {heatmap_path}')

    passed_wells_path = os.path.join(output_folder, f'{file_name}_passed_wells.csv')
    pd.DataFrame(pass_wells, columns=['Passed Wells']).to_csv(passed_wells_path, index=False)
    print(f'✓ Passed wells saved to: {passed_wells_path}')

    return pass_wells, fail_wells

def main():
    file_path = input("Enter the path to your CSV file: ")

    while True:
        if not os.path.exists(file_path):
            print(f"✗ File not found: '{file_path}'")
        elif os.path.isdir(file_path):
            print(f"✗ That's a folder, not a file. Please include the filename (e.g. /Users/you/Desktop/data.csv)")
        elif not file_path.lower().endswith('.csv'):
            print(f"✗ File must be a .csv file")
        else:
            break
        file_path = input("Enter the path to your CSV file: ")

    output_folder = input("Enter the name of the output folder to save results: ").strip()
    os.makedirs(output_folder, exist_ok=True)
    print(f'✓ Output folder ready: {output_folder}')

    threshold = float(input("Enter the threshold value for pass/fail: ").strip())

    table_data = data_table(file_path)
    pass_wells, fail_wells = heat_map(table_data, threshold, file_path, output_folder)

if __name__ == "__main__":
    main()