`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   16:24:44 04/03/2022
// Design Name:   mux2_8bit
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_mux2_8bit.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: mux2_8bit
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////
`include "mux2_8bit.v"

module test_mux2_8bit;

	// Inputs
	reg a_addr;
	reg [7:0] a;
	reg b_addr;
	reg [7:0] b;
	reg c_addr;
	reg [7:0] c;
	reg d_addr;
	reg [7:0] d;

	// Outputs
	wire [7:0] o;

	// Instantiate the Unit Under Test (UUT)
	mux2_8bit uut (
		.a_addr(a_addr), 
		.a(a), 
		.b_addr(b_addr), 
		.b(b), 
		.c_addr(c_addr), 
		.c(c), 
		.d_addr(d_addr), 
		.d(d), 
		.o(o)
	);

	initial begin
		// Initialize Inputs
		a_addr = 0;
		a = 8'haa;
		b_addr = 0;
		b = 8'hbb;
		c_addr = 0;
		c = 8'hcc;
		d_addr = 0;
		d = 8'hdd;

		// Wait 100 ns for global reset to finish
		#10;
		// Add stimulus here
		#1 if (o != 0) begin
		   $display("Errro, expected o == 0");
			$finish;
		end
		
		#1 a_addr = 1;
		#1 if (o != 8'haa) begin
		   $display("Error, expected o == 8'haa");
			$finish;
		end
		
		#1 a_addr = 0;
		#1 b_addr = 1;
		#1 if (o != 8'hbb) begin
		   $display("Error, expected o == 8'hbb");
			$finish;
		end
		
		#1 b_addr = 0;
		#1 c_addr = 1;
		#1 if (o != 8'hcc) begin
		   $display("Error, expected o == 8'hcc");
			$finish;
		end
		
		#1 c_addr = 0;
		#1 d_addr = 1;
		#1 if (o != 8'hdd) begin
		   $display("Error, expected o == 8'hdd");
			$finish;
		end
		
		#1 d_addr = 0;
		#1 if (o != 8'h00) begin
		   $display("Error, expected o == 8'h00");
			$finish;
		end		
      $finish;
	end
      
endmodule
