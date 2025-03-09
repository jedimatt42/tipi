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

`include "tipi_4bit_pi_bus.v"
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
		// run test tasks
		test_read_TD();
		test_read_TC();
		test_write_RD();
		test_write_RC();
		$display("Success");
		$finish;
	end

	// Task for testing reading TD
	task test_read_TD;
	begin  
	   $display("Test: reading TD");
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
			$finish;
		end

		// Test Reading TD
		TD = 8'hA5;

		// - clock in the register select for TD
		force data = 4'b0000;
		#10;
		send_clk();
      release data;

      // - the high nibble should be available
		#10;

		// - verify the high nibble
		if (data !== TD[7:4]) begin
			$display("Error: High nibble of TD is not visible on data, %h", data);
			$finish;
		end

		// clock out the low nibble
		send_clk();

		// - verify the low nibble
		if (data !== TD[3:0]) begin
			$display("Error: Low nibble of TD is not visible on data, %h", data);
			$finish;
		end
	end
	endtask
      
	// Task for testing reading TC
	task test_read_TC;
	begin  
	   $display("Test: reading TC");
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
			$finish;
		end

		// Test Reading TC
		TC = 8'h5A;

		// - clock in the register select for TC
		force data = 4'b0001;
		#10;
		send_clk();
      release data;

        // - the high nibble should be available
		#10;

		// - verify the high nibble
		if (data !== TC[7:4]) begin
			$display("Error: High nibble of TC is not visible on data");
			$finish;
		end

		// clock out the low nibble
		send_clk();

		// - verify the low nibble
		if (data !== TC[3:0]) begin
			$display("Error: Low nibble of TC is not visible on data");
			$finish;
		end
	end
	endtask
	
	// Test write of RD
	task test_write_RD;
	begin
	   $display("Test: write RD");
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
			$finish;
		end
	   // - clock in the register select for RD
		force data = 4'b0010;
		#10;
		send_clk();
      release data;
		
		// - clock in the high nibble for RD
		force data = 4'b1010;
		#10;
		send_clk();
		release data;
		
		// - clock in the low nibble for RD
		force data = 4'b0101;
		#10;
		send_clk();
		release data;
		
		// Verify RD value
		if (RD !== 8'b10100101) begin
			$display("Error: RD register not set correctly");
         $finish;
		end
	end
	endtask
	
	// Test write of RC
	task test_write_RC;
	begin
	   $display("Test: write RC");
		// Test reset
		reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
         $finish();
		end
	   // - clock in the register select for RC
		force data = 4'b0011;
		#10;
		send_clk();
      release data;
		
		// - clock in the high nibble for RC
		force data = 4'b0101;
		#10;
		send_clk();
		release data;
		
		// - clock in the low nibble for RC
		force data = 4'b1010;
		#10;
		send_clk();
		release data;
		
		// Verify RC value
		if (RC !== 8'b01011010) begin
			$display("Error: RC register not set correctly");
			$finish();
		end	
	end
	endtask
	
	task send_clk;
	begin
	   clk = 1;
		#10;
		clk = 0;
		#10;
	end
	endtask
	
	task send_reset;
	begin
	   reset = 1;
		#10; // Wait for 10 ns
      reset = 0;
		#10; // Wait for 10 ns

		// Verify state
		if (data !== 4'bz) begin
			$display("Error: data is not in input mode after reset");
         $finish();
		end
	end
	endtask
endmodule

