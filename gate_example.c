#include <stdint.h>
#include <stdio.h>

// Допустим у гейта 64 входа, тогда даже если у него 1 выход, то 2^64 бит данных = 2*2^60 байт = 2 Эксабайта.
// Поэтому входы гейтов не могут быть больше 64 бит.

const uint8_t gate_example_table[2][4] = {
    { 0x12, 0x34, 0x56, 0x78 },
    { 0xAB, 0xCD, 0xEF, 0x01 },
};

const uint8_t gate_and_table[4][1] = {
    { 0x00 },
    { 0x00 },
    { 0x00 },
    { 0x01 }
};

const uint8_t gate_or_table[4][1] = {
    { 0x00 },
    { 0x01 },
    { 0x01 },
    { 0x01 }
};

const uint8_t *calc_gate(const uint8_t (*table)[1], uint64_t in)
{
    return table[in];
}

void move_bit(uint8_t *dst, uint8_t dst_addr, const uint8_t *src, uint8_t src_addr)
{
    const uint8_t src_byte = src_addr >> 3;
    const uint8_t src_bit  = src_addr & 7;
    const uint8_t dst_byte = dst_addr >> 3;
    const uint8_t dst_bit  = dst_addr & 7;

    const uint8_t bit  = (uint8_t)((src[src_byte] >> src_bit) & 1);
    const uint8_t mask = (uint8_t)(1 << dst_bit);

    dst[dst_byte] = (uint8_t)((dst[dst_byte] & ~mask) | (uint8_t)(bit << dst_bit));
}

void set_bit(uint64_t *dst, uint8_t dst_bit, const uint8_t *src, uint8_t src_addr)
{
    const uint8_t src_byte = src_addr >> 3;
    const uint8_t src_bit  = src_addr & 7;

    const uint8_t bit   = (uint8_t)((src[src_byte] >> src_bit) & 1);
    const uint64_t mask = (((uint64_t)1) << dst_bit);

    *dst = ((*dst & ~mask) | (((uint64_t)bit) << dst_bit));
}

void calc(const uint8_t in [], uint8_t out [])
{
    uint64_t A_in = 0;
    set_bit(&A_in, 0, in, 0);
    set_bit(&A_in, 1, in, 1);
    const uint8_t *A = calc_gate(gate_and_table, A_in);

    uint64_t B_in = 0;
    set_bit(&B_in, 0, A, 0);
    set_bit(&B_in, 1, in, 2);
    const uint8_t *B = calc_gate(gate_or_table, B_in);

    move_bit(out, 0, B, 0);
}

void print_bin(uint8_t value, int len)
{
    while((len--) > 0)
    {
        putchar('0' + (value & 1));
        value >>= 1;
    }
}

int main()
{
    uint8_t out = 0;
    for(uint8_t in = 0; in < 8; in++)
    {
        calc(&in, &out);
        print_bin(in, 3);
        printf(" -> ");
        print_bin(out, 1);
        printf("\n");
    }
}
