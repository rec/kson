#include <vector>
#include <kson/Tokenizer.h>

#define CATCH_CONFIG_MAIN
#include <catch/catch.hpp>

namespace kson {

using Results = std::vector<std::string>;

Results runTest(std::string s) {
    Results results;

    auto callback = [&](Span span) {
        // std::cout << "'" << span.first << ", " << span.second << '\n';
        results.push_back(std::string(span.first, span.second - span.first));
    };

    tokenize(callback, Span{&s.front(), 1 + &s.back()});
    return results;
}

TEST_CASE( "Tokenizer Trivial", "" ) {
    auto results = runTest("");
    REQUIRE(results.empty());
}

TEST_CASE( "Tokenizer Whitespace", "" ) {
    auto results = runTest(" \n\t\r\n\t");
    REQUIRE(results.empty());
}

TEST_CASE( "Tokenizer Word", "" ) {
    auto results = runTest(" word " );
    REQUIRE( results.size() == 1 );
    REQUIRE( results[0] == "word" );
}

TEST_CASE( "Tokenizer Quotes", "" ) {
    auto results = runTest(" ' he\\llo, \\'wor\"ld!\\' ' word");
    REQUIRE( results.size() == 2 );
    REQUIRE( results[0] == "' he\\llo, \\'wor\"ld!\\' '" );
    REQUIRE( results[1] == "word" );
}

TEST_CASE( "Tokenizer Double Quotes", "" ) {
    auto results = runTest(" ' he\\llo, \\'wor\"ld!\\' ' \"wo\\\"rd\" ");
    REQUIRE( results.size() == 2 );
    REQUIRE( results[0] == "' he\\llo, \\'wor\"ld!\\' '" );
    REQUIRE( results[1] == "\"wo\\\"rd\"" );
}

TEST_CASE( "Tokenizer Quote in word", "" ) {
    auto results = runTest(" wo'rd'nes ");
    REQUIRE( results.size() == 3 );
    REQUIRE( results[0] == "wo");
    REQUIRE( results[1] == "'rd'");
    REQUIRE( results[2] == "nes");
}

}  // kson
