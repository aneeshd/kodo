// Copyright Steinwurf ApS 2011-2013.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

//! [0]
#include <kodo/rlnc/full_rlnc_codes.hpp>
//! [0]

int main()
{
    //! [1]

    // Set the number of symbols (i.e. the generation size in RLNC
    // terminology) and the size of a symbol in bytes
    uint32_t max_symbols = 16;
    uint32_t max_symbol_size = 1400;

    //! [1]

    typedef kodo::full_rlnc_encoder<fifi::binary8> rlnc_encoder;
    typedef kodo::full_rlnc_decoder<fifi::binary8> rlnc_decoder;

    // In the following we will make an encoder/decoder factory.
    // The factories are used to build actual encoders/decoders
    rlnc_encoder::factory encoder_factory(max_symbols, max_symbol_size);
    auto encoder = encoder_factory.build();

    rlnc_decoder::factory decoder_factory(max_symbols, max_symbol_size);
    auto decoder = decoder_factory.build();

    std::vector<uint8_t> payload(encoder->payload_size());
    std::vector<uint8_t> block_in(encoder->block_size());

    // Just for fun - fill the data with random data
    for(auto &e: block_in)
        e = rand() % 256;

    // Assign the data buffer to the encoder so that we may start
    // to produce encoded symbols from it
    encoder->set_symbols(sak::storage(block_in));

    uint32_t encoded_count = 0;

    while( !decoder->is_complete() )
    {
        // Encode a packet into the payload buffer
        uint32_t bytes_used = encoder->encode( &payload[0] );
        std::cout << "Bytes used = " << bytes_used << std::endl;

        ++encoded_count;

        // Pass that packet to the decoder
        decoder->decode( &payload[0] );
    }

    std::cout << "Encoded count = " << encoded_count << std::endl;

    return 0;

}
