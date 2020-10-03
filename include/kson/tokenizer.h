#pragma once

#include <ctype.h>
#include <string>

namespace kson {

using CharPtr = const char*;
using Span = std::pair<CharPtr, CharPtr>;

template <typename Callback>
void tokenize(Callback, Span);

namespace token {

enum class State {
    between,
    word,
    singleQuote,
    doubleQuote,
    singleBackslash,
    doubleBackslash,
    comment,
    emit
};

using StateChange = State(*)(char, char);

inline
State between(char ch, char) {
    if (isspace(ch))
        return State::between;
    if (ch == '\'')
        return State::singleQuote;
    if (ch == '"')
        return State::doubleQuote;
    if (ch == '#')
        return State::comment;
    return State::word;
}

inline
State word(char ch, char next) {
    return (isspace(ch) or isspace(next)) ? State::emit : State::word;
}

inline
State singleQuote(char ch, char) {
    if (ch == '\'')
        return State::emit;
    if (ch == '\\')
        return State::singleBackslash;
    return State::singleQuote;
}

inline
State doubleQuote(char ch, char) {
    if (ch == '"')
        return State::emit;
    if (ch == '\\')
        return State::doubleBackslash;
    return State::doubleQuote;
}

inline
State singleBackslash(char, char) {
    return State::singleQuote;
}

inline
State doubleBackslash(char, char) {
    return State::doubleQuote;
}

inline
State comment(char ch, char) {
    return (ch == '\n') ? State::emit : State::comment;
}

template <typename Callback>
void tokenize(Callback callback, Span span) {
    static const StateChange CHANGES[] = {
        &between,
        &word,
        &singleQuote,
        &doubleQuote,
        &singleBackslash,
        &doubleBackslash,
        &comment
    };

    CharPtr token;
    auto state = State::between;

    for (auto i = span.first; i != span.second; ++i) {
        if (state == State::between)
            token = i;

        auto isEnd = (i == span.second - 1);
        auto ch = i[0];
        auto next = isEnd ? '\0' : i[1];
        auto stateChange = CHANGES[static_cast<int>(state)];
        state = stateChange(ch, next);

        if (isEnd or state == State::emit) {
            callback({token, i + 1});
            state = State::between;
        }
    }
}

}  // namespace token

template <typename Callback>
void tokenize(Callback callback, Span span) {
    token::tokenize(callback, span);
}

}  // namespace kson
