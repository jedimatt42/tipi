`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   04:26:59 03/29/2022
// Design Name:   shift_nib_in_pout
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_shift_nib_in_pout.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: shift_nib_in_pout
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////
`include "shift_nib_in_pout.v"

module test_shift_nib_in_pout;

	// Inputs
	reg clk;
	reg select;
	reg le;
	reg [0:3] din;

	// Outputs
	wire [0:7] dout;

	// Instantiate the Unit Under Test (UUT)
	shift_nib_in_pout uut (
		.clk(clk), 
		.select(select), 
		.le(le), 
		.din(din), 
		.dout(dout)
	);

	initial begin
		// Initialize Inputs
		clk = 0;
		select = 0;
		le = 0;
		din = 0;

		// Wait 100 ns for global reset to finish
		#10;

		// Add stimulus here
      #1 select = 1;
		#1 clk = 1;
		#1 clk = 0;
		#1 clk = 1;
		#1 clk = 0;
		#1 le = 1;
		#1 clk = 1;
		#1 clk = 0;
		#1 le = 0;		
		#1 if (dout != 0) begin
		  $display("Error expected to latch 0");
		  $finish;
		end
        
		#1 din = 4'hF;
		#1 clk = 1;
		#1 clk = 0;		
		#1 if (dout != 0) begin
		  $display("Error expected to latch 0");
		  $finish;
		end

		#1 din = 4'h5;
		#1 clk = 1;
		#1 clk = 0;
		#1 if (dout != 0) begin
		  $display("Error expected to latch 0");
		  $finish;
		end
		
		#1 din = 4'h0; // shouldn't affect latch operation
		
		#1 le = 1;
		clk = 1;
		#1 clk = 0;
		#1 le = 0;
		
		#1 if (dout != 8'hF5) begin
		    $display("Error, expected dout == 8'hF5");
			 $finish;
		end
		
		select = 0;
		// Cannot test for z state of dout, but can observe it.
		#1 select = 0;
		
		$finish;
	end
      
endmodule

