#pragma once

#include "types.hh"
#include <string>

enum AstType {
#define x(Name, ...) Name,
AST_TYPES
#undef x
};

enum AstType getAstType(std::string& str);
