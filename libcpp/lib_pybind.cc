#include <args.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace pybind11::literals;

namespace py = pybind11;

PYBIND11_MODULE(libcpp, m) {
  py::class_<somelib::Args>(m, "args")
    .def(py::init<>())
    .def_readwrite("input", &somelib::Args::input)
    .def_readwrite("output", &somelib::Args::output)
    .def(
      "parseArgs",
      [](somelib::Args& m, const std::vector<std::string> args) {
        m.parseArgs(args);
      })
    .def(
      "dumpArgs",
      [](somelib::Args& m) {
        return m.dumpArgs();
      });
}