`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   20:03:06 03/27/2022
// Design Name:   latch_8bit
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_latch_8bit.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: latch_8bit
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

`include "latch_8bit.v"

module test_latch_8bit;

	// Inputs
	reg le;
	reg [0:7] din;

	// Outputs
	wire [0:7] dout;

	// Instantiate the Unit Under Test (UUT)
	latch_8bit uut (
		.le(le), 
		.din(din), 
		.dout(dout)
	);

	initial begin
		// Initialize Inputs
		le = 0;
		din = 0;

		// Wait 10 ns for global reset to finish
		#10 if (dout != 0) begin
		  $display("not initialized properly");
		  $finish;
		end
        
		// Add stimulus here
      #1 din = 8'hAA;
 		#1 le = 1;
      #1 le = 0;
		#1 if (dout != 8'hAA) begin
		  $display("Error dout not 8'hAA");
		  $finish;
		end
		
		#1 din = 8'h00;
		#1 if (dout != 8'hAA) begin
		  $display("Error dout not 8'hAA");
		  $finish;
		end
		
		#1 le = 1;
		#1 if (dout != 0) begin
		  $display("Error dout not 0");
		  $finish;
		end
		$finish;
end
      
endmodule

