# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    """Cocotb test for tt_um_dco2"""

    dut._log.info("Start")

    # Set the clock period to 10us (100KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset Sequence
    dut._log.info("Reset")
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut.ena.value = 1

    dut._log.info("Testing project behavior")

    # Apply test values matching Verilog testbench
    test_values = [0b00000000, 0b00000001, 0b00000010, 0b00000100,
                   0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]

    for val in test_values:
        dut.ui_in.value = val
        await ClockCycles(dut.clk, 32)

        # Assertion: Modify this based on expected module behavior
        expected_value = val  # Assuming uo_out should follow ui_in
        assert dut.uo_out.value == expected_value, f"Mismatch: ui_in={val:08b}, uo_out={dut.uo_out.value:08b}"

    # Second Reset Cycle Test
    dut._log.info("Testing Reset Behavior")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    # Final Log & Finish
    dut._log.info("Test completed successfully.")
