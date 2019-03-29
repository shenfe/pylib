#include "args.h"

#include <stdlib.h>

#include <iostream>
#include <stdexcept>

namespace somelib {

Args::Args() {}

void Args::parseArgs(const std::vector<std::string>& args) {
  for (int ai = 2; ai < args.size(); ai += 2) {
    if (args[ai][0] != '-') {
      std::cerr << "Provided argument without a dash! Usage:" << std::endl;
      printHelp();
      exit(EXIT_FAILURE);
    }
    try {
      if (args[ai] == "-h") {
        std::cerr << "Here is the help! Usage:" << std::endl;
        printHelp();
        exit(EXIT_FAILURE);
      } else if (args[ai] == "-input") {
        input = std::string(args.at(ai + 1));
      } else if (args[ai] == "-output") {
        output = std::string(args.at(ai + 1));
      } else {
        std::cerr << "Unknown argument: " << args[ai] << std::endl;
        printHelp();
        exit(EXIT_FAILURE);
      }
    } catch (std::out_of_range) {
      std::cerr << args[ai] << " is missing an argument" << std::endl;
      printHelp();
      exit(EXIT_FAILURE);
    }
  }
}

void Args::printHelp() {
  std::cerr << "\nThe following arguments are mandatory:\n"
            << "  -input              input file path\n"
            << "  -output             output file path\n";
}

std::string Args::dumpArgs() {
  return "input " + input + "\n" + "output " + output + "\n";
}

} // namespace somelib