# libpy

> Python库项目模板，兼容Python2/3，支持C++扩展。

## installation

```sh
$ pip install .
```

安装后，python的site-packages目录下会多出如下文件：

```
├── libcpp.so
├── libpy/
└── libpy-x.y.z.dist-info/
```

## usage

### command line

```sh
$ libpy
$ libpy fn1 --help
$ libpy --config-json '{}' fn1
$ libpy --config-file ./demo/some-config.json fn1
$ libpy fn1 < ./demo/some-config.json
```

### python api

```py
import libpy
```
