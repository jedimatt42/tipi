`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   17:50:51 03/08/2025
// Design Name:   crubits
// Module Name:   /home/ise/dev/gitlab/jedimatt42/tipi/hardware/tipi-peb/ise/test_crubits.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: crubits
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////
`include "crubits.v"
module test_crubits;

	// Inputs
	reg [0:3] cru_base;
	reg ti_cru_clk;
	reg ti_memen;
	reg ti_ph3;
	reg [0:14] addr;
	reg ti_cru_out;

	// Outputs
	wire ti_cru_in;
	wire [0:3] bits;

	// Instantiate the Unit Under Test (UUT)
	crubits uut (
		.cru_base(cru_base), 
		.ti_cru_clk(ti_cru_clk), 
		.ti_memen(ti_memen), 
		.ti_ph3(ti_ph3), 
		.addr(addr), 
		.ti_cru_out(ti_cru_out), 
		.ti_cru_in(ti_cru_in), 
		.bits(bits)
	);

	initial begin
		// Initialize Inputs
		cru_base = 4'b0000;
		ti_cru_clk = 0;
		ti_memen = 0;
		ti_ph3 = 0;
		addr = 0;
		ti_cru_out = 0;

		// Wait 100 ns for global reset to finish
		#100;

		// Verify initial state of bits
		if (bits !== 4'b0000) begin
			$display("Error: expected all cru bits unset");
		end else begin
			$display("Success: all cru bits are unset");
		end

		// Add stimulus here

        // When addr is 0x1000, and cru_base is 0x0, then verify we read cru bit 0 as unset.
		addr = 15'h1000;
		ti_cru_out = 1;
		#10
		ti_cru_clk = 1;
		#10
		ti_cru_clk = 0;
		#10
		
		// Verify state of bits
		if (bits !== 4'b1000) begin
			$display("Error: expected all cru bits unset");
		end else begin
			$display("Success: all cru bits are unset");
		end


	end
      
endmodule

