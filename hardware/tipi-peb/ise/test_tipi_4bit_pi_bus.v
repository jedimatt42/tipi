`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   11:37:37 03/01/2025
// Design Name:   tipi_4bit_pi_bus
// Module Name:   /home/ise/dev/gitlab/jedimatt42/tipi/hardware/tipi-peb/ise/test_tipi_4bit_pi_bus.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: tipi_4bit_pi_bus
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

`include "tipi_4bit_pi_bus.v"
module test_tipi_4bit_pi_bus;

	// Inputs
	reg clk;
	reg reset;
	reg [7:0] TD;
	reg [7:0] TC;

	// Outputs
	wire [7:0] RD;
	wire [7:0] RC;

	// Bidirs
	wire [3:0] data;

	// Instantiate the Unit Under Test (UUT)
	tipi_4bit_pi_bus uut (
		.clk(clk),
		.reset(reset),
		.data(data),
		.TD(TD),
		.TC(TC),
		.RD(RD),
		.RC(RC)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		reset = 0;
		TD = 0;
		TC = 0;

		// Wait 100 ns for global reset to finish
		#100;
		// run test tasks
		test_read_TD();
		test_read_TC();
	end

	// Task for testing reading TD
	task test_read_TD;
	begin  
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
		end else begin
			$display("Success: data is in input mode after reset");
		end

		// Test Reading TD
		TD = 8'hA5;

		// - clock in the register select for RD
		force data = 4'b0000;
		#10;
		clk = 1;
		#10;
		clk = 0;
		#10;
      release data;

      // - clock out the high nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the high nibble
		if (data !== TD[7:4]) begin
			$display("Error: High nibble of TD is not visible on data");
		end else begin
			$display("Success: High nibble of TD is visible on data");
		end

		// clock out the low nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the low nibble
		if (data !== TD[3:0]) begin
			$display("Error: Low nibble of TD is not visible on data");
		end else begin
			$display("Success: Low nibble of TD is visible on data");
		end
	end
	endtask
      
	// Task for testing reading TC
	task test_read_TC;
	begin  
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
		end else begin
			$display("Success: data is in input mode after reset");
		end

		// Test Reading TC
		TC = 8'h5A;

		// - clock in the register select for TC
		force data = 4'b0001;
		#10;
		clk = 1;
		#10;
		clk = 0;
		#10;
      release data;

        // - clock out the high nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the high nibble
		if (data !== TC[7:4]) begin
			$display("Error: High nibble of TC is not visible on data");
		end else begin
			$display("Success: High nibble of TC is visible on data");
		end

		// clock out the low nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the low nibble
		if (data !== TC[3:0]) begin
			$display("Error: Low nibble of TC is not visible on data");
		end else begin
			$display("Success: Low nibble of TC is visible on data");
		end
	end
	endtask  
endmodule

