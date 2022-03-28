`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:30:25 03/27/2022
// Design Name:   shift_pload_nib_out
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_shift_pload_nib_out.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: shift_pload_nib_out
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////
`include "shift_pload_nib_out.v"

module test_shift_pload_nib_out;

	// Inputs
	reg clk;
	reg select;
	reg le;
	reg [7:0] data;

	// Outputs
	wire [3:0] nout;

	// Instantiate the Unit Under Test (UUT)
	shift_pload_nib_out uut (
		.clk(clk), 
		.select(select), 
		.le(le), 
		.data(data), 
		.nout(nout)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		select = 0;
		le = 0;
		data = 0;
		#1 select = 1;
		#1 le = 1;
		#1 clk = 1;
		#1 clk = 0;
		#1 select = 0;
		#1 le = 0;
		
		#1 select = 1;
		#1 data = 8'hAF;
		#1 if (nout != 4'h0) begin
		    $display("Error: premature load, expected 0");
			 $finish;
		end
		
		// first clock out loads from input register.
		#1 le = 1;
		#1 clk = 1;
		#1 clk = 0;
		#1 le = 0;
		#1 if (nout != 4'hA) begin
		    $display("Error: expected bits 7:4 4'hA");
			 $finish;
		end
		
		#1 clk = 1;
		#1 clk = 0;
		#1 if (nout != 4'hF) begin
		    $display("Error: expected bits 3:0 4'hF");
			 $finish;
		end
		
		#1 clk = 1;
		#1 clk = 0;
		#1 if (nout != 4'h0) begin
		    $display("Error: expected 0 after already shifting everything out");
			 $finish;
		end
		
      $finish;		
	end
endmodule

