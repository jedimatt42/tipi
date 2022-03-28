`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   05:45:18 03/29/2022
// Design Name:   tristate_8bit
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_tristate_8bit.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: tristate_8bit
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

`include "tristate_8bit.v"

module test_tristate_8bit;

	// Inputs
	reg T;
	reg [7:0] I;

	// Outputs
	wire [7:0] O;

	// Instantiate the Unit Under Test (UUT)
	tristate_8bit uut (
		.T(T), 
		.I(I), 
		.O(O)
	);

	initial begin
		// Initialize Inputs
		T = 0;
		I = 0;

		// Wait 1 ns for global reset to finish
		#1;
		#1 if (O != 8'bZ) begin
		    $display("Error: expecte Z");
			 $finish;
		end
        
		// Add stimulus here
		#1 T = 1;
		#1 I = 8'hA5;
		#1 if (O != 8'hA5) begin
		    $display("Error: expected output 8'hA5");
			 $finish;
		end
		#1 I = 8'hFF;
		#1 if (O != 8'hFF) begin
		    $display("Error: expected output 8'hA5");
			 $finish;
		end
		
		$finish;
	end
      
endmodule

