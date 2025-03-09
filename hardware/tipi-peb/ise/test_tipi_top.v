`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   17:37:45 04/03/2022
// Design Name:   tipi_top
// Module Name:   /home/ise/ise_projects/tipi/hardware/tipi-peb/ise/test_tipi_top.v
// Project Name:  tipi
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: tipi_top
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module test_tipi_top;

	// Inputs
	reg [0:3] crub;
	reg r_clk;
	reg r_le;
	reg ti_cruclk;
	reg ti_dbin;
	reg ti_memen;
	reg ti_we;
	reg ti_ph3;
	reg [0:15] ti_a;

	// Outputs
	wire led0;
	wire db_dir;
	wire db_en;
	wire dsr_b0;
	wire dsr_b1;
	wire dsr_en;
	wire r_reset;
	wire ti_cruin;
	wire ti_extint;

	// Bidirs
	wire [0:3] r_nib;
	wire [0:7] tp_d;
	
	reg inout_control = 1;
	reg [3:0] r_nib_in = 0;
	assign r_nib = inout_control ? r_nib_in : 4'bz;
	
	reg dbusio_control = 1;
	reg [7:0] dbus_in = 0;
	assign tp_d = dbusio_control ? dbus_in : 8'bz;

	// Instantiate the Unit Under Test (UUT)
	tipi_top uut (
		.led0(led0), 
		.crub(crub), 
		.db_dir(db_dir), 
		.db_en(db_en), 
		.dsr_b0(dsr_b0), 
		.dsr_b1(dsr_b1), 
		.dsr_en(dsr_en), 
		.r_clk(r_clk), 
		.r_le(r_le), 
		.r_nib(r_nib), 
		.r_reset(r_reset), 
		.ti_cruclk(ti_cruclk), 
		.ti_dbin(ti_dbin), 
		.ti_memen(ti_memen), 
		.ti_we(ti_we), 
		.ti_ph3(ti_ph3), 
		.ti_cruin(ti_cruin), 
		.ti_extint(ti_extint), 
		.ti_a(ti_a), 
		.tp_d(tp_d)
	);
		
	initial begin
		// Initialize Inputs
	    crub = 4'hf;
	    r_clk = 0;
	    r_le = 0;
	    ti_cruclk = 1;
	    ti_dbin = 1;
	    ti_memen = 1;
	    ti_we = 1;
	    ti_ph3 = 1;
	    ti_a = 16'h0000;

		// Wait 10 ns for global reset to finish
		#10;
		#1 if (r_reset != 1) begin
		    $display("Error, r_reset output should be high");
		    $finish;
		end
		
		// TEST enable crubit 0;
		#1 ti_a = 16'h1001;
		#1 ti_cruclk = 0;
		#1 ti_cruclk = 1;
		#1 if (uut.cru_state[0] != 1) begin
		    $display("Error, crubit 0 should be set");
			$finish;
		end
		
		// TEST set cru reset bit
	   #1 ti_a = 16'h1003;
		#1 ti_cruclk = 0;
		#1 ti_cruclk = 1;
		#1 if (uut.cru_state[1] != 1) begin
		    $display("Error, crubit 1 (reset) should be set");
			$finish;
		end
		#1 if (r_reset != 0) begin
		    $display("Error, r_reset output should be low");
			$finish;
		end
		
		// TEST clear cru reset bit
		#1 ti_a = 16'h1002;
		#1 ti_cruclk = 0;
		#1 ti_cruclk = 1;
		#1 if (r_reset != 1) begin
		    $display("Error, r_reset output should be high");
		    $finish;
		end
		
		// Read TD
		#1 ti_a = 16'h5fff;
		#1 ti_memen = 0;
		#1 if (tp_d != 8'h00) begin
		    $display("Error, 5fff should be 0");
			$finish;
		end
		// Write TD
		#1 dbus_in = 8'hff;
		#1 dbusio_control = 1;
		#1 ti_memen = 0;
		#1 ti_we = 0;
		#1 ti_we = 1;
		#1 ti_memen = 1;
		#1 dbusio_control = 0;
		#1 ti_a = 16'h0000;
		// Re-Read TD
		
		#1 dbus_in = 8'h00;
		#1 ti_a = 16'h5fff;
		#1 ti_memen = 0;
		#1 if (db_dir != 1) begin
		    $display("Error, db_dir should be 1");
			$finish;
		end
		#1 if (tp_d != 8'hff) begin
		    $display("Error, 5fff should be ff");
			$finish;
		end
		#1 ti_memen = 1;
		
	    #10;
        $finish;
	end
      
endmodule
