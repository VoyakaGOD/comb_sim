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

#ifdef COMB_SIM_NO_X
    const uint8_t *calc_gate(const uint8_t *table, uint8_t outw, uint64_t in)
    {
        return table + (outw * in);
    }
#endif

#ifdef COMB_SIM_X_OPT
    const uint8_t *calc_gate(const uint8_t *table, uint8_t outw, uint64_t in, uint64_t in_u, uint8_t *out_u)
    {
        uint8_t *seen0 = out_u;
        uint8_t *seen1 = out_u + outw;
        
        uint64_t xbits[64] = {0};
        uint8_t xcount = 0;
        for(uint8_t i = 0; i < 64; i++)
            if((in_u >> i) & 1)
                xbits[xcount++] = (uint64_t)1 << i;

        uint64_t in_clean = in & ~in_u;
        uint64_t N = (uint64_t)1 << xcount;
        for (uint64_t n = 0; n < N; n++)
        {
            uint64_t possible_in = in_clean;
            for (uint8_t i = 0; i < xcount; i++)
                if ((n >> i) & 1)
                    possible_in |= xbits[i];

            const uint8_t *value = table + (possible_in * outw);
            for (uint8_t i = 0; i < outw; i++)
            {
                seen0[i] |= ~value[i];
                seen1[i] |= value[i];
            }
        }

        for(uint8_t i = 0; i < outw; i++)
            out_u[i] = seen0[i] & seen1[i];
        return table + (outw * in_clean);
    }
#endif

#ifdef COMB_SIM_X_PESS
    const uint8_t *calc_gate(const uint8_t *table, uint8_t outw, uint64_t in, uint64_t in_u, uint8_t *out_u)
    {
        uint8_t x = (in_u != 0) ? 0xff : 0;
        for(uint8_t i = 0; i < outw; i++)
            out_u[i] = x;
        return table + (outw * in);
    }
#endif
