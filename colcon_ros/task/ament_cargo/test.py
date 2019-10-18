# Copyright 2016-2018 Dirk Thomas
# Copyright 2019 Ruffin White
# Licensed under the Apache License, Version 2.0


from colcon_cargo.task.cargo.test import CargoTestTask
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.task import TaskExtensionPoint

logger = colcon_logger.getChild(__name__)


class AmentCargoTestTask(TaskExtensionPoint):
    """Test ROS packages with the build type 'ament_cargo'."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    async def test(self):  # noqa: D102
        args = self.context.args
        logger.info(
            "Testing ROS package in '{args.path}' with build type "
            "'ament_cargo'".format_map(locals()))

        # reuse CMake test task
        extension = CargoTestTask()
        extension.set_context(context=self.context)
        return await extension.test()
