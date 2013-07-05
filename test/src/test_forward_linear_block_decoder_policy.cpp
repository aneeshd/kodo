// Copyright Steinwurf ApS 2011-2013.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

/// @file test_forward_linear_block_decoder_policy.cpp Unit test
///       for the forward_linear_block_decoder_policy

#include <cstdint>
#include <gtest/gtest.h>

#include <kodo/forward_linear_block_decoder_policy.hpp>


/// Run the tests typical coefficients stack
TEST(TestForwardLinearBlockDecoderPolicy, test_functions)
{

    {
        kodo::forward_linear_block_decoder_policy policy(0, 5);
        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 0U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 1U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 2U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 3U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 4U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), false);
        EXPECT_EQ(policy.index(), 5U);
        policy.advance();

        EXPECT_EQ(policy.at_end(), true);

        EXPECT_EQ(kodo::forward_linear_block_decoder_policy::max(1,2), 2);
        EXPECT_EQ(kodo::forward_linear_block_decoder_policy::min(1,2), 1);
    }
}



