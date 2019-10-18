# Copyright 2019-2018 Dirk Thomas
# Copyright 2019 Ruffin White
# Licensed under the Apache License, Version 2.0

import os

from colcon_cargo.task.cargo.build import CargoBuildTask
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.shell import get_shell_extensions
from colcon_core.task import TaskExtensionPoint
from colcon_ros.task import add_app_to_cpp

logger = colcon_logger.getChild(__name__)


class AmentCargoBuildTask(TaskExtensionPoint):
    """Build ROS packages with the build type 'ament_cargo'."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    # def add_arguments(self, *, parser):  # noqa: D102
    #     parser.add_argument(
    #         '--ament-cargo-args',
    #         nargs='*', metavar='*', type=str.lstrip,
    #         help="Pass arguments to 'ament_cargo' packages. "
    #         'Arguments matching other options must be prefixed by a space,\n'
    #         'e.g. --ament-cargo-args " --help"')

    async def build(self):  # noqa: D102
        args = self.context.args
        logger.info(
            "Building ROS package in '{args.path}' with build type "
            "'ament_cargo'".format_map(locals()))

        # reuse Cargo build task with additional logic
        extension = CargoBuildTask()
        extension.set_context(context=self.context)

        # add a hook for each available shell
        additional_hooks = []
        shell_extensions = get_shell_extensions()
        file_extensions = []
        for shell_extensions_same_prio in shell_extensions.values():
            for shell_extension in shell_extensions_same_prio.values():
                file_extensions += shell_extension.get_file_extensions()
        for file_extension in sorted(file_extensions):
            additional_hooks.append(
                'share/{self.context.pkg.name}/local_setup.{file_extension}'
                .format_map(locals()))

        # additional arguments
        if args.test_result_base:
            if args.cargo_args is None:
                args.cargo_args = []
            # ament_cargo appends the project name itself
            # FIXME: Find cargo equivalent
            # args.cargo_args.append(
            #     '-DAMENT_TEST_RESULTS_DIR=' +
            #     os.path.dirname(args.test_result_base))
        if args.symlink_install:
            if args.cargo_args is None:
                args.cargo_args = []
            # FIXME: Find cargo equivalent
            # args.cargo_args.append('-DAMENT_CMAKE_SYMLINK_INSTALL=1')
        if args.ament_cargo_args:
            if args.cargo_args is None:
                args.cargo_args = []
            args.cargo_args += args.ament_cargo_args

        return await extension.build(
            environment_callback=add_app_to_cpp,
            additional_hooks=additional_hooks)
