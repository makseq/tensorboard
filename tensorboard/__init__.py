# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""TensorBoard is a webapp for understanding TensorFlow runs and graphs.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorboard import lazy


# Please be careful when changing the structure of this file.
#
# The lazy imports in this file must use `importlib.import_module`, not
# `import tensorboard.foo` or `from tensorboard import foo`, or it will
# be impossible to reload the TensorBoard module without breaking these
# top-level public APIs. This has to do with the gory details of
# Python's module system. Take `tensorboard.notebook` as an example:
#
#   - When the `tensorboard` module (that's us!) is initialized, its
#     `notebook` attribute is initialized to a new LazyModule. The
#     actual `tensorboard.notebook` submodule is not loaded.
#
#   - When the `tensorboard.notebook` submodule is first loaded, Python
#     _reassigns_ the `notebook` attribute on the `tensorboard` module
#     object to point to the underlying `tensorboard.notebook` module
#     object, rather than its former LazyModule value. This occurs
#     whether the module is loaded via the lazy module or directly as an
#     import:
#
#       - import tensorboard; tensorboard.notebook.start(...)  # one way
#       - from tensorboard import notebook  # other way; same effect
#
#   - When the `tensorboard` module is reloaded, its `notebook`
#     attribute is once again bound to a (new) LazyModule, while the
#     `tensorboard.notebook` module object is unaffected and still
#     exists in `sys.modules`. But then...
#
#   - When the new LazyModule is forced, it must resolve to the existing
#     `tensorboard.notebook` module object rather than itself (which
#     just creates a stack overflow). If the LazyModule load function
#     uses `import tensorboard.notebook; return tensorboard.notebook`,
#     then the first statement will do _nothing_ because the
#     `tensorboard.notebook` module is already loaded, and the second
#     statement will return the LazyModule itself. The same goes for the
#     `from tensorboard import notebook` form. We need to ensure that
#     the submodule is loaded and then pull the actual module object out
#     of `sys.modules`... which is exactly what `importlib` handles for
#     us.
#
# See <https://github.com/tensorflow/tensorboard/issues/1989> for
# additional discussion.


@lazy.lazy_load('tensorboard.notebook')
def notebook():
  import importlib  # pylint: disable=g-import-not-at-top
  return importlib.import_module('tensorboard.notebook')


@lazy.lazy_load('tensorboard.program')
def program():
  import importlib  # pylint: disable=g-import-not-at-top
  return importlib.import_module('tensorboard.program')


@lazy.lazy_load('tensorboard.summary')
def summary():
  import importlib  # pylint: disable=g-import-not-at-top
  return importlib.import_module('tensorboard.summary')
