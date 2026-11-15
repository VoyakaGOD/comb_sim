#include <stdint.h>

// Допустим у гейта 64 входа, тогда даже если у него 1 выход, то 2^64 бит данных = 2*2^60 байт = 2 Эксабайта.
// Поэтому входы гейтов не могут быть больше 64 бит.

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
