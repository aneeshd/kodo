// Copyright Steinwurf ApS 2011-2012.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

#pragma once

#include "systematic_encoder.hpp"
#include "storage_aware_systematic_phase.hpp"

namespace kodo
{

    /// @brief Implements a systematic encoder where the default
    /// behavior is not to produce and systematic symbols
    template<class SuperCoder>
    class default_off_systematic_encoder :
        public systematic_encoder<false,
               storage_aware_systematic_phase<SuperCoder> >
    { };

}


