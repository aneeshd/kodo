// Copyright Steinwurf ApS 2011-2013.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

/// @file test_has_systematic_encoder.cpp Unit tests for the
///       has_systematic_encoder class

#include <cstdint>

#include <gtest/gtest.h>

#include <kodo/set_systematic_off.hpp>
#include <kodo/rlnc/full_vector_codes.hpp>

namespace kodo
{

    // Put dummy layers and tests classes in an anonymous namespace
    // to avoid violations of ODF (one-definition-rule) in other
    // translation units
    namespace
    {

        struct dummy
        {
            void set_systematic_off()
            {
                m_systematic_off = false;
            }

            bool m_systematic_off;
        };

    }
}

TEST(TestSetSystematicOff, set)
{

    {
        kodo::dummy d;
        d.m_systematic_off = true;

        kodo::set_systematic_off(d);
        EXPECT_FALSE(d.m_systematic_off);
    }

    {
        typedef kodo::full_rlnc_encoder<fifi::binary8> encoder_type;

        encoder_type::factory factory(10,10);
        auto encoder = factory.build();

        EXPECT_TRUE(encoder->is_systematic_on());

        kodo::set_systematic_off(encoder);
        EXPECT_FALSE(encoder->is_systematic_on());
    }



}



