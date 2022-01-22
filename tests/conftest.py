import pytest

import diskspacemonitor.models as models


@pytest.fixture()
def crash_dump_50():

    total_storage, current_storage_used = 100, 50

    crash_dump = models.Agent(
        name="CrashDumpStore", total_available_storage=total_storage
    )

    crash_dump.set_current_storage_useage(current_storage_used)

    return crash_dump
