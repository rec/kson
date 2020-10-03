#pragma once

#include <ctype.h>
#include <cstring>
#include <string>
#include <kson/Types.h>

namespace kson {

template <typename Callback>
void splitToken(Callback callback, Span span) {
    static auto punctuation = "[{}],:";

    if (*span.first == '\'' or *span.first == '"') {
        callback(span);
        return;
    }

    auto token = span.first;
    for (auto i = span.first; i != span.second; ++i) {
        char ch = i[0];
        char next = (i + 1 != span.second) ? i[1] : '\0';

        if (strchr(punctuation, ch) or strchr(punctuation, next)) {
            callback({token, i + 1});
            token = i + 1;
        }
    }

    if (token != span.second)
        callback({token, span.second});
}

}  // namespace kson
