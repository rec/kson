#pragma once

#include <kson/tokenizer.h>

#define CATCH_CONFIG_MAIN
#include <catch/catch.hpp>

TEST_CASE( "Tokenizer compiles", "" ) {
    REQUIRE( Factorial(1) == 1 );
    REQUIRE( Factorial(2) == 2 );
    REQUIRE( Factorial(3) == 6 );
    REQUIRE( Factorial(10) == 3628800 );
}
