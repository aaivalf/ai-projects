import os
import re
import subprocess


def write_prover9_input(board, filename):
    #directory path
    prover9_bin_path = "/home/daria/Documents/Prover9/LADR-2009-11A/bin/"
    full_path = os.path.join(prover9_bin_path, filename)
    with open(full_path, "w") as file:
        file.write("assign(max_seconds,30).\n")
        file.write("set(binary_resolution).\n")
        file.write("set(print_gen).\n\n")

        file.write("formulas(assumptions).\n")
        file.write("    all x all y (safe(x, y) <-> -mine(x, y)).\n")

        for cell in board:
            if cell.is_opened:
                file.write(f"    safe({cell.x}, {cell.y}).\n")
            if cell.is_mine_candidate:
                file.write(f"    mine({cell.x}, {cell.y}) | safe({cell.x}, {cell.y}).\n")
            if cell.surrounded_cells_mines_length == 0:
                for surrounding_cell in cell.surrounded_cells:
                    if not surrounding_cell.is_opened:
                        file.write(f"    safe({surrounding_cell.x}, {surrounding_cell.y}).\n")
        file.write("end_of_list.\n")

        file.write("formulas(goals).\n")
        file.write("    safe(x, y).\n")
        file.write("end_of_list.\n")
    print(f"Prover9 input written to: {full_path}")

def run_prover9(input_file):

    prover9_path = "/home/daria/Documents/Prover9/LADR-2009-11A/bin/prover9"
    prover9_path = os.path.expanduser(prover9_path)
    try:
        command = f"{prover9_path} -f {input_file}"
        result = subprocess.run(
            command,
            cwd=os.path.dirname(prover9_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        print("Prover9 Output:")
        print(result.stdout)
        if result.stderr:
            print(f"Prover9 Error: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"Error running Prover9: {e}")
        return None

def parse_prover9_output(output):
    safe_cells = set()

    for line in output.splitlines():
        line = line.strip()
        # Use regex to extract safe(x, y) from Prover9 output
        match = re.match(r"safe\((\d+),\s*(\d+)\)\.", line)
        if match:
            try:
                x, y = map(int, match.groups())
                safe_cells.add((x, y))
            except ValueError:
                print(f"Skipping invalid line: {line}")
        elif "SEARCH FAILED" in line:
            print("No further logical deductions possible.")
            break

    safe_cells = sorted(list(safe_cells))

    print("Parsed Safe Cells:", safe_cells)
    return safe_cells


def get_safe_cells_from_prover9(board):
    input_file = "minesweeper.in"
    write_prover9_input(board, input_file)
    output = run_prover9(input_file)
    if output:
        safe_cells = parse_prover9_output(output)
        if not safe_cells:
            print("No safe cells deduced by Prover9.")
        return safe_cells
    else:
        return []
