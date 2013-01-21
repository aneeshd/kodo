// Copyright Steinwurf ApS 2011-2012.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

#include <ctime>

#include <gtest/gtest.h>

#include <kodo/object_decoder.hpp>
#include <kodo/object_encoder.hpp>
#include <kodo/rfc5052_partitioning_scheme.hpp>
#include <kodo/rlnc/full_vector_codes.hpp>
#include <kodo/has_shallow_symbol_storage.hpp>
#include <kodo/has_deep_symbol_storage.hpp>

template<
    class Encoder,
    class Decoder,
    class Partitioning,
    class ObjectData
    >
void invoke_object(uint32_t max_symbols, uint32_t max_symbol_size, uint32_t multiplier)
{

    typedef kodo::object_encoder<Encoder, Partitioning, ObjectData> object_encoder;
    typedef kodo::object_decoder<Decoder, Partitioning> object_decoder;

    std::vector<char> data_in(max_symbols * max_symbol_size * multiplier);
    std::vector<char> data_out(max_symbols * max_symbol_size * multiplier, '\0');

    kodo::random_uniform<char> fill_data;
    fill_data.generate(&data_in[0], data_in.size());

    typename Encoder::factory encoder_factory(max_symbols, max_symbol_size);
    typename Decoder::factory decoder_factory(max_symbols, max_symbol_size);

    object_encoder obj_encoder(encoder_factory, kodo::storage(data_in));
    object_decoder obj_decoder(decoder_factory, obj_encoder.object_size());

    EXPECT_EQ(multiplier, obj_encoder.encoders());
    EXPECT_EQ(multiplier, obj_decoder.decoders());
    EXPECT_TRUE(obj_encoder.encoders() == obj_decoder.decoders());


    for(uint32_t i = 0; i < obj_encoder.encoders(); ++i)
    {
        typename Encoder::pointer encoder = obj_encoder.build(i);
        typename Decoder::pointer decoder = obj_decoder.build(i);

        if(kodo::is_systematic_encoder(encoder))
            kodo::set_systematic_off(encoder);

        // Since the storage we encode is a multiple of the
        // block size we always expect that the encoder is
        // fully "filled" with data
        EXPECT_EQ(encoder->block_size(), encoder->bytes_used());
        EXPECT_EQ(decoder->block_size(), decoder->bytes_used());

        EXPECT_EQ(encoder->payload_size(), decoder->payload_size());

        std::vector<uint8_t> payload(encoder->payload_size());

        while(!decoder->is_complete())
        {
            encoder->encode( &payload[0] );
            decoder->decode( &payload[0] );

        }

        kodo::mutable_storage storage = kodo::storage(
            &data_out[0] + (i * encoder->block_size()), encoder->block_size());

        kodo::copy_symbols(storage, decoder);

    }

    EXPECT_TRUE(std::equal(data_in.begin(), data_in.end(), data_out.begin()));

}


// template
// <
//     class Encoder,
//     class Decoder,
//     class Partitioning
// >
// void invoke_object_partial(uint32_t max_symbols,
//                            uint32_t max_symbol_size,
//                            uint32_t multiplier)
// {

//     uint32_t object_size = max_symbols * max_symbol_size * multiplier;
//     object_size -= (rand() % object_size);

//     typedef kodo::object_encoder<Encoder, Partitioning> object_encoder;
//     typedef kodo::object_decoder<Decoder, Partitioning> object_decoder;

//     std::vector<char> data_in(object_size);
//     std::vector<char> data_out(object_size, '\0');

//     kodo::random_uniform<char> fill_data;
//     fill_data.generate(&data_in[0], data_in.size());

//     typename Encoder::factory encoder_factory(max_symbols, max_symbol_size);
//     typename Decoder::factory decoder_factory(max_symbols, max_symbol_size);

//     object_encoder obj_encoder(encoder_factory, kodo::storage(data_in));
//     object_decoder obj_decoder(decoder_factory, obj_encoder.object_size());

//     EXPECT_TRUE(obj_encoder.encoders() >= 1);
//     EXPECT_TRUE(obj_decoder.decoders() >= 1);
//     EXPECT_TRUE(obj_encoder.encoders() == obj_decoder.decoders());

//     uint32_t bytes_used = 0;

//     for(uint32_t i = 0; i < obj_encoder.encoders(); ++i)
//     {
//         typename Encoder::pointer encoder = obj_encoder.build(i);
//         typename Decoder::pointer decoder = obj_decoder.build(i);

//         if(kodo::is_systematic_encoder(encoder))
//             kodo::set_systematic_off(encoder);

//         EXPECT_TRUE(encoder->block_size() >= encoder->bytes_used());
//         EXPECT_TRUE(decoder->block_size() >= decoder->bytes_used());

//         EXPECT_TRUE(encoder->block_size() == decoder->block_size());
//         EXPECT_TRUE(encoder->bytes_used() == decoder->bytes_used());
//         EXPECT_TRUE(encoder->payload_size() == decoder->payload_size());

//         std::vector<uint8_t> payload(encoder->payload_size());

//         while(!decoder->is_complete())
//         {
//             encoder->encode( &payload[0] );
//             decoder->decode( &payload[0] );

//         }

//         kodo::mutable_storage storage = kodo::storage(
//             &data_out[0] + bytes_used, decoder->bytes_used());

//         kodo::copy_symbols(storage, decoder);

//         bytes_used += decoder->bytes_used();
//     }

//     EXPECT_EQ(bytes_used, object_size);
//     EXPECT_TRUE(std::equal(data_in.begin(), data_in.end(), data_out.begin()));

// }



// void test_object_coders(uint32_t symbols, uint32_t symbol_size, uint32_t multiplier)
// {
//     invoke_object<
//         kodo::full_rlnc2_encoder,
//         kodo::full_rlnc2_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

//     invoke_object<
//         kodo::full_rlnc8_encoder,
//         kodo::full_rlnc8_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

//     invoke_object<
//         kodo::full_rlnc16_encoder,
//         kodo::full_rlnc16_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

//     invoke_object_partial<
//         kodo::full_rlnc2_encoder,
//         kodo::full_rlnc2_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

//     invoke_object_partial<
//         kodo::full_rlnc8_encoder,
//         kodo::full_rlnc8_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

//     invoke_object_partial<
//         kodo::full_rlnc16_encoder,
//         kodo::full_rlnc16_decoder,
//             kodo::rfc5052_partitioning_scheme>(symbols, symbol_size, multiplier);

// }


// TEST(TestObjectCoder, construct_and_invoke_the_basic_api)
// {
//     test_object_coders(32, 1600, 2);
//     test_object_coders(1, 1600, 2);

//     srand(static_cast<uint32_t>(time(0)));

//     uint32_t symbols = (rand() % 256) + 1;
//     uint32_t symbol_size = ((rand() % 100) + 1) * 16;

//     // Multiplies the data to be encoded so that the object encoder
//     // is expected to contain multiplier encoders.
//     uint32_t multiplier = (rand() % 10) + 1;

//     test_object_coders(symbols, symbol_size, multiplier);
// }

#include <type_traits>

namespace kodo
{

    
template<class EncoderType>
class storage_reader
{
public:

    typedef typename EncoderType::pointer pointer;
    
public:

    storage_reader(const const_storage &storage)
        : m_storage(storage)
        {
            assert(m_storage.m_size > 0);
            assert(m_storage.m_data != 0);
        }

    uint32_t size() const
        {
            return m_storage.m_size;
        }

    void read(pointer &encoder, uint32_t offset, uint32_t size)
        {
            assert(encoder);
            assert(offset < m_storage.m_size);
            assert(size > 0);
            
            uint32_t remaining_bytes = m_storage.m_size - offset;
            
            assert(size <= remaining_bytes);
            
            const_storage storage;
            storage.m_data = m_storage.m_data + offset;
            storage.m_size = size;
            
            encoder->set_symbols(storage);
            
            // We require that encoders includes the has_bytes_used
            // layer to support partially filled encoders
            encoder->set_bytes_used(size);
        }
    

private:

    const_storage m_storage;
    
};

    
}
// template<template <class> class T, class Coder>
// inline void has_layer(const Coder& coder)
// {
//     std::cout << std::is_base_of<T, Coder>::value << std::endl;
// }

// class object_reader
// {
// public:

//     template<template <class> class T, class U>
//     void read(kodo::symbol_storage_shallow<T,U> &shallow)
//         {
//             std::cout << "Works" << std::endl;
//         }
    
// };

// template
// <
//     class EncoderType,
//     class BlockPartitioning
// >
// class storage_encoder : public object_encoder<EncoderType, BlockPartitioning>
// {

    
// };






// TEST(TestObjectCoder, test_object_reader)
// {
//     typedef kodo::full_rlnc8_encoder encoder_t;

//     encoder_t::factory f(10,10);
//     encoder_t::pointer e = f.build(10,10);

//     typedef kodo::full_rlnc8_decoder decoder_t;
        
//     decoder_t::factory fd(10,10);
//     decoder_t::pointer d = fd.build(10,10);

//     // std::cout << "Has shallow " << kodo::has_shallow_storage(e) << std::endl;
//     // std::cout << "Has shallow " << kodo::has_shallow_storage(d) << std::endl;

//     std::cout << kodo::has_shallow_symbol_storage<encoder_t>::value << std::endl;
//     std::cout << kodo::has_shallow_symbol_storage<decoder_t>::value << std::endl;
    
//     static_assert(kodo::has_shallow_symbol_storage<encoder_t>::value,
//                   "Mush use shallow");

//     object_reader reader(10,10);
//     //reader(10,10,d);
    
// }











