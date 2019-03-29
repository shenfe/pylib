#pragma once

#include <istream>
#include <ostream>
#include <string>
#include <vector>

namespace somelib {

class Args {
 public:
  Args();

  std::string input;
  std::string output;

  void parseArgs(const std::vector<std::string>& args);
  void printHelp();
  std::string dumpArgs();
};

} // namespace somelib