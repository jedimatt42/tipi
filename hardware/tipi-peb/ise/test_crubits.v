`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   04:20:51 04/03/2022
// Design Name:   crubits
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_crubits.v
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
		ti_cru_clk = 1;
		ti_memen = 1;
		ti_ph3 = 0;
		ti_cru_out = 0;

		// Wait 10 ns for global reset to finish
		#10;
        
		$display("Test: set crubit 0");
		addr = 15'b000100000000000;
      #1 ti_cru_out = 1;
		#1 ti_cru_clk = 0;
		#1 ti_cru_clk = 1;
		#1 if (bits != 4'b1000) begin
		   $display("Error, cru bit 0 not set");
			$finish;
		end

      $display("Test: set crubit 1");
		addr = 15'b000100000000001;
      #1 ti_cru_out = 1;
		#1 ti_cru_clk = 0;
		#1 ti_cru_clk = 1;
		#1 if (bits != 4'b1100) begin
		   $display("Error, cru bit 1 not set");
			$finish;
		end

      $display("Test: set crubit 2");
		addr = 15'b000100000000010;
      #1 ti_cru_out = 1;
		#1 ti_cru_clk = 0;
		#1 ti_cru_clk = 1;
		#1 if (bits != 4'b1110) begin
		   $display("Error, cru bit 2 not set");
			$finish;
		end

      $display("Test: set crubit 3");
		addr = 15'b000100000000011;
      #1 ti_cru_out = 1;
		#1 ti_cru_clk = 0;
		#1 ti_cru_clk = 1;
		#1 if (bits != 4'b1111) begin
		   $display("Error, cru bit 3 not set");
			$finish;
		end
		
		$display("Success");
		$finish;
	end
      
endmodule
