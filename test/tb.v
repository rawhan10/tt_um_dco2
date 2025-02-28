`default_nettype none
`timescale 1ns / 1ps

module tb ();

  // Dump VCD for waveform analysis
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
  end

  // Signals
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] dco_code;
  wire [7:0] ui_in;
  wire [7:0] uo_out;
  wire [7:0] uio_in, uio_out, uio_oe;

	`ifdef GL_TEST
   supply1 VPWR; // Define VPWR as a logic '1'
   supply0 VGND; // Define VGND as a logic '0'
   `endif

  // Instantiate DCO module
  tt_um_dco2 user_project (
	`ifdef GL_TEST
      .VPWR(VPWR), // Power
      .VGND(VGND), // Ground
      `endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // Enable signal
      .clk    (clk),      // Clock
      .rst_n  (rst_n)     // Active-low reset
  );

  assign ui_in = dco_code; // Assign dco_code to ui_in

  // Generate 50MHz clock (20ns period)
  always #10 clk = ~clk;

  initial begin
    clk = 0;
    rst_n = 0; // Assert reset
    ena = 0;
    dco_code = 8'b00000000;

    // Hold reset for 50ns
    #50 rst_n = 1; ena = 1; 

    // Wait for the design to stabilize
    #100;

    // Start changing dco_code values
    #2000 dco_code = 8'b00000001;
    #2000 dco_code = 8'b00000010;
    #2000 dco_code = 8'b00000100;
    #2000 dco_code = 8'b00001000;
    #2000 dco_code = 8'b00010000;
    #2000 dco_code = 8'b00100000;
    #2000 dco_code = 8'b01000000;
    #2000 dco_code = 8'b10000000;

    // Reset again and check behavior
    #500 rst_n = 0;
    #500 rst_n = 1;

    // Wait and then finish simulation
    #5000;
    $finish;
  end

  // Monitor changes
  initial begin
    $monitor("Time=%0t | ui_in=%b, uo_out=%b | reset=%b | clk=%b",
             $time, ui_in, uo_out, rst_n, clk);
  end

endmodule
