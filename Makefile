# Optional command line arguments:
# see http://stackoverflow.com/a/24264930/43839
#
# For an optimized, stripped build, you might use:
#
#   $ make OPTIMIZE=-O3 SYMBOLS="" DEFINES=""
#
# For a Clang C++11 build, use:
#
#   $ make COMPILER=g++ STDLIB=c++11
#

COMPILER ?= g++
DEFINES ?= -DDEBUG
OPTIMIZE ?= -O0
STDLIB ?= c++17
SYMBOLS ?= -g

#
# Compilation variables.
#
DEPENDENCIES = -MMD -MP -MF

CXX = $(COMPILER)

MACRO_DEFINITIONS = \
 -DBUILD_TIMESTAMP="\"`date +\"%Y-%m-%d %H:%I:%M\"`\"" \
 -DGIT_COMMIT_ID=\""`git log --format=\"%H\" -n 1`"\" \
 $(DEFINES) \

COMPILATION = $(OPTIMIZE) $(SYMBOLS) -std=$(STDLIB) -pthread
INCLUDE_PATHS = -I ./include
LIBRARIES = -lm -lstdc++
WARNINGS = -Wall -Wextra -Wno-strict-aliasing -Wpedantic -Wno-nested-anon-types

CXXFLAGS_BASE += \
  $(MACRO_DEFINITIONS) \
  $(COMPILATION) \
  $(INCLUDE_PATHS) \
  $(WARNINGS)

CXXFLAGS = $(CXXFLAGS_BASE) $(DEPENDENCIES)

TARGET_EXEC ?= tests

BUILD_DIR ?= ./build
SRC_DIRS ?= ./src
INC_DIR ?= ./include

SRCS := $(shell find $(SRC_DIRS) -name *.cpp -or -name *.c -or -name *.s)
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

CPPFLAGS ?=_DIR) -MMD -MP

$(BUILD_DIR)/$(TARGET_EXEC): $(OBJS)
	$(CXX) -lpthread $^ -o $@ $(CXXFLAGS) $(LIBRARIES) $(LDFLAGS)

$(BUILD_DIR)/%.cpp.o: %.cpp
	$(MKDIR_P) $(dir $@)
	$(CXX) -c $< -o $@ $(CXXFLAGS)
#   $(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@


.PHONY: clean

clean:
	$(RM) -r $(BUILD_DIR)

-include $(DEPS)

MKDIR_P ?= mkdir -p
