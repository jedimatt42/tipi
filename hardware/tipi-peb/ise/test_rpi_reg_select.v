`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   06:37:18 03/29/2022
// Design Name:   rpi_reg_select
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_rpi_reg_select.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: rpi_reg_select
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

`include "rpi_reg_select.v"

module test_rpi_reg_select;

	// Inputs
	reg reset;
	reg clk;
	wire [3:0]reg_sel;
	reg [3:0]din;

	// Instantiate the Unit Under Test (UUT)
	rpi_reg_select uut (
		.reset(reset), 
		.clk(clk),
		.din(din),
		.reg_sel(reg_sel)
	);
	
	initial begin
		// Initialize Inputs
		reset = 0;
		clk = 0;
		din = 4'hf;

		// Wait 10 ns for global reset to finish
		#10;
        
		// Add stimulus here
      #1 reset = 1;
		#1 reset = 0;
		#1 if (reg_sel != 0) begin
		   $display("Error: failed to reset register select");
			$finish;
		end
		
		#1 din = 4'h1;
		#1 clk = 1;
		#1 clk = 0;
		#1 if (reg_sel != 4'h1) begin
		   $display("Error: expected 4'h1");
			$finish;
		end
		
		#1 din = 4'hf;
		#1 clk = 1;
		#1 clk = 0;
		#1 if (reg_sel != 4'h1) begin
		   $display("Error: 2nd clk should be ignored");
			$finish;
		end
		
		#1 clk = 1;
		#1 clk = 0;
		#1 if (reg_sel != 4'h1) begin
		   $display("Error: 3rd clk should be ignored");
			$finish;
		end
		
		#1 clk = 1;
		#1 clk = 0;
		#1 if (reg_sel != 4'hf) begin
		   $display("Error: next should wrap to clk 0");
			$finish;
		end

      $finish;
	end
      
endmodule

