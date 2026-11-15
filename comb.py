import json
from sys import argv
from placer import *

def chunks(value : int, n: int = 8):
    if value == 0:
        yield "0x00"
    while value > 0:
        dec = value % (10**n)
        value //= (10**n)
        yield f"0x{int(str(dec), 2):02X}"

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
        out_size = (outw + 7) // 8
        tables += f"#define GATE_{gate_name}_OUTW {out_size}\n"
        tables += f"const uint8_t gate_{gate_name}_table[{1 << inw}][{out_size}] = {{\n"
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

    if "schematics" not in json_obj:
        print("No schematics in source json !!!")
        return -1

    gg = GateGraph(json_obj["schematics"])

    for i in [2, 3]:
        with open(argv[i], "w") as x_file:
            x_file.write(f"#define COMB_SIM_X_{"OPT" if i == 2 else "PESS"}\n")
            x_file.write(header)
            x_file.write(generate_gate_tables(json_obj))
            placer = UndefinedPlacer(lambda s: x_file.write(s), 4 - i)
            placer(gg)

    if len(argv) > 4:
        with open(argv[4], "w") as no_x_file:
            no_x_file.write("#define COMB_SIM_NO_X\n")
            no_x_file.write(header)
            no_x_file.write(generate_gate_tables(json_obj))
            placer = DefinedPlacer(lambda s: no_x_file.write(s))
            placer(gg)

    return 0

if __name__ == "__main__":
    main()
