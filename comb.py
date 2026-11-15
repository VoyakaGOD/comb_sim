import json
from sys import argv

def chunks(value : int, n: int = 8):
    if value == 0:
        yield "0x0"
    while value > 0:
        dec = value % (10**n)
        value //= (10**n)
        yield hex(int(str(dec), 2))

def generate_gate_tables(json_obj : dict) -> str:
    if "gates" not in json_obj:
        return "// No gates in source json !!!"
    tables = "\n"
    for gate_name in json_obj["gates"]:
        gate_description = json_obj["gates"][gate_name]
        if "inw" not in gate_description:
            tables += f"//{gate_name} has no [inw]"
            continue
        if "outw" not in gate_description:
            tables += f"//{gate_name} has no [outw]"
            continue
        if "table" not in gate_description:
            tables += f"//{gate_name} has no [table]"
            continue
        inw = gate_description["inw"]
        outw = gate_description["outw"]
        tables += f"const uint8_t gate_{gate_name}_table[{1 << inw}][{(outw + 7) // 8}] = {{\n"
        lines = []
        for out in gate_description["table"]:
            lines.append("    { " + ", ".join(chunks(int(out))) + " }")
        tables += ",\n".join(lines) + "\n};\n\n"
    return tables

def main() -> int:
    if len(argv) < 4:
        print("Usage: [python] comb.py <in> <out-x-opt> <out-x-pess> [out-no-x]")
        return -1

    with open("header.c", "r") as file:
        header = file.read()

    with open(argv[1], "r") as input_file:
        json_obj : dict = json.load(input_file)

    with open(argv[3], "w") as x_pess_file:
        x_pess_file.write(header)
        x_pess_file.write(generate_gate_tables(json_obj))

    return 0

if __name__ == "__main__":
    main()
