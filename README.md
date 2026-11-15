# comb-sim

A small tool for simulating combinational logic circuits described in JSON.

It parses a circuit description, analyze graph of gates and create
compilable C function `calc`, that evaluates the circuit for given input values.

## Usage

`(python) comb.py <in> <out-x-opt> <out-x-pess> [out-no-x]`

| Argument | Meaning |
|---|---|
| `<in>` | Input JSON file (see `examples/`) |
| `<out-x-opt>` | Path to the generated C file, optimistic X-mode |
| `<out-x-pess>` | Path to the generated C file, pessimistic X-mode |
| `[out-no-x]` | Optional path to the generated C file, plain two-valued mode |

- **`<out-x-opt>` — optimistic.** The heaviest mode. X propagation is resolved
  by brute-forcing every possible assignment of the undefined input bits and
  keeping only the output bits whose value is the same across all assignments;
  the rest are marked `X`.
- **`<out-x-pess>` — pessimistic.** Any `X` on any input bit forces every
  output bit of that gate to `X`.
- **`out-no-x` — two-valued.** No X support at all; inputs are assumed to be
  fully defined.

## Important note

Files in examples/ are provided as sample inputs for the Python
script - they demonstrate the expected JSON format, not necessarily
functionally correct circuits.
