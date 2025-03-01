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
        
		// Add stimulus here

	end
      
endmodule

