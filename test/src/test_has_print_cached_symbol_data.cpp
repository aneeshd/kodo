// Copyright Steinwurf ApS 2011-2013.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

/// @file test_has_trace_decode_symbol.cpp Unit tests for the
///       has_trace_decode_symbol class

#include <cstdint>

#include <gtest/gtest.h>

#include <kodo/has_print_cached_symbol_data.hpp>
#include <kodo/rlnc/full_rlnc_codes.hpp>
#include <kodo/rlnc/on_the_fly_codes.hpp>

/// @todo  review this unit test
TEST(TestHasPrintCachedSymbolData, detect)
{
    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_encoder<fifi::binary> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_encoder<fifi::binary8> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_decoder<fifi::binary> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_decoder<fifi::binary8> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::on_the_fly_encoder<fifi::binary> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::on_the_fly_encoder<fifi::binary8> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::on_the_fly_decoder<fifi::binary> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::on_the_fly_decoder<fifi::binary8> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_encoder<fifi::binary> >::value);

    EXPECT_FALSE(kodo::has_print_cached_symbol_data<
                     kodo::full_rlnc_encoder<fifi::binary8> >::value);

}
