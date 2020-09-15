#pragma once

#include <ctype.h>
#include <utility>

namespace kson {

namespace detail {

template <typename Ptr>
struct Range {
    Ptr begin, end;
    size_t size() const { return end - begin; }

    template <typename T>
    void copy(T from, T to) const {
        std::copy(from + begin, from + end, to);  // Test for overlapping
    }
};

using StringView = Range<const char*>;

class Queue {
  public:
    Queue() = default;

    size_t size() const {
        return range_.size();
    }

    const char* begin() const { return &buf_[range_.begin]; }
    const char* end() const { return &buf_[range_.end]; }

    bool advance(size_t n) {
        auto empty = n < range_.size();
        if (empty)
            range_.begin += n;
        else
            range_ = {);
        return empty;
    }

    char pop() {
        char ch{};
        if (size()) {
            ch = *begin();
            advance(1);
        }
        return ch;
    }

    void push(StringView in) {
        auto lacking = int64(in.size()) - buf_.size() - range_.end;
        if (lacking > range_.begin) {
            auto size = buf_.size();
            auto delta = std::max(size_t(lacking), size / 2);
            buf_.resize(size + delta);
        } else if (lacking > 0) {
            std::copy(begin(), end(), buf_.begin());
            range_ = {0, range_.size()};
        }

        in.copy(0, buf_.begin() + buf_.end());
        range_.end += in.size();
    }

  private:
    std::string buf_;
    Range<size_t> range_ = {};
};

}  // detail


class Parser {
  public:
    enum class State {
        before,
        inComment,
        afterLiteral,
    };

    Parser() = default;

    const std::string& error() const { return error_; }

    template <typename Callback>
    bool parseOnce(Callback cb) {
        if (not (queue_.size() and error.empty()))
            return false;

        auto ch = queue_.pop();
        switch (state) {
            case before: {
                break;
            }
            case inComment: {
                break;
            }
            case afterLiteral: {
                break;
            }
            }
        }
    }

  private:
    char head() const { return buf_[

    Offset skipWhitespace() {
        Offset result{};
        while (hasQueue()) {
        }
    }

    State state_ = State::before;
    Span token_ = {};

    Queue buf_;
    std::string error_;
};

}  // namespace kson
