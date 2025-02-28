# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


@cocotb.test()
async def test_project(dut):
    """High-Quality Cocotb Testbench for tt_um_dco2"""

    dut._log.info("Test Start")

    # Initialize Clock (10us Period → 100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset Sequence
    dut._log.info("Resetting Design")
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Test Input Patterns
    test_values = [0b00000000, 0b00000001, 0b00000010, 0b00000100,
                   0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]

    for val in test_values:
        dut.ui_in.value = val
        await ClockCycles(dut.clk, 5)  # Wait before checking output

        # Ensure Output is Stable Before Assertion
        for _ in range(3):  # Check for multiple cycles
            await RisingEdge(dut.clk)

        actual_value = dut.uo_out.value.integer  # Convert to integer
        expected_value = val  # Modify based on actual design behavior

        dut._log.info(f"ui_in={val:08b}, Expected uo_out={expected_value:08b}, Actual uo_out={actual_value:08b}")

        assert actual_value == expected_value, f"Mismatch: ui_in={val:08b}, uo_out={actual_value:08b}"

    # Test Reset Behavior Again
    dut._log.info("Testing Reset Again")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    dut._log.info("Test Completed Successfully")
