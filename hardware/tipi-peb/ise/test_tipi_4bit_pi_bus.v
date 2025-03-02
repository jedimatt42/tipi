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
	end

	// Task for testing reading RD
	task test_read_RD;
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

		// Test Reading RD
		RD = 8'hA5;

		// - clock in the register select for RD
		force data = 4'b0010;
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
		if (data !== RD[7:4]) begin
			$display("Error: High nibble of RD is not visible on data");
		end else begin
			$display("Success: High nibble of RD is visible on data");
		end

		// clock out the low nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the low nibble
		if (data !== RD[3:0]) begin
			$display("Error: Low nibble of RD is not visible on data");
		end else begin
			$display("Success: Low nibble of RD is visible on data");
		end
	end
	endtask
      
	// Task for testing reading RC
	task test_read_RD;
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

		// Test Reading RC
		RC = 8'h5A;

		// - clock in the register select for RC
		force data = 4'b0011;
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
		if (data !== RC[7:4]) begin
			$display("Error: High nibble of RD is not visible on data");
		end else begin
			$display("Success: High nibble of RD is visible on data");
		end

		// clock out the low nibble
		clk = 1;
		#10;
		clk = 0;
		#10;

		// - verify the low nibble
		if (data !== RC[3:0]) begin
			$display("Error: Low nibble of RD is not visible on data");
		end else begin
			$display("Success: Low nibble of RD is visible on data");
		end
	end
	endtask  
endmodule

