#!/usr/bin/env python3
"""Check Dhrystone's split and legacy core layouts."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import run_dhrystone


class CoreLayoutTests(unittest.TestCase):
    def test_legacy_flat_core_uses_its_root_for_rtl_and_roms(self):
        with tempfile.TemporaryDirectory() as directory:
            core = Path(directory)
            self.assertEqual(run_dhrystone.core_layout(core), (core, core))

    def test_split_core_uses_separate_rtl_and_rom_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            core = Path(directory)
            (core / "rtl").mkdir()
            (core / "src").mkdir()
            for name in ("ucode.hex", "pla_entry_rom.hex", "pla_group_entry.hex"):
                (core / "src" / name).touch()
            self.assertEqual(
                run_dhrystone.core_layout(core), (core / "rtl", core / "src")
            )

    def test_incomplete_split_core_does_not_reuse_stale_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            core = root / "core"
            (core / "rtl").mkdir(parents=True)
            build = root / "build" / "z486_current"
            (build / "obj_dir").mkdir(parents=True)
            (build / "obj_dir" / "Vtb_dhrystone").touch()
            stale_rom = build / "ucode.hex"
            stale_rom.write_text("stale\n")

            with mock.patch.object(run_dhrystone, "BUILD_DIR", root / "build"):
                with self.assertRaisesRegex(FileNotFoundError, "ROM source directory"):
                    run_dhrystone.build_core("z486_current", core)

                (core / "src").mkdir()
                (core / "src" / "ucode.hex").touch()
                with self.assertRaisesRegex(FileNotFoundError, "pla_entry_rom.hex"):
                    run_dhrystone.build_core("z486_current", core)

            self.assertEqual(stale_rom.read_text(), "stale\n")


if __name__ == "__main__":
    unittest.main()
