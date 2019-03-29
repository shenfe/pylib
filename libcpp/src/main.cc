#include <iomanip>
#include <iostream>
#include <queue>
#include <stdexcept>
#include "args.h"

using namespace somelib;

int main(int argc, char** argv) {
  std::vector<std::string> args(argv, argv + argc);
  Args a = Args();
  a.parseArgs(args);
  std::cout << a.dumpArgs() << std::endl;
  return 0;
}
