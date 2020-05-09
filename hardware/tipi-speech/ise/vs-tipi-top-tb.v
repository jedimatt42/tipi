`timescale 1ns / 100ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   16:41:52 05/03/2020
// Design Name:   tipi_top
// Module Name:   C:/Users/jgpar/Documents/TI99/TIPI/VS-TIPI-CPLD/vs-tipi-top-tb.v
// Project Name:  vs-tipi
// Target Device:  xc95144xl
// Tool versions:  ISE 14.1
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

module vs_tipi_top_tb;

	// Inputs
	reg [0:3] crub;
	reg r_clk;
	reg r_cd;
	reg r_dout;
	reg r_le;
	reg r_rt;
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
	wire dram_a0;
	wire dram_en;
	wire r_din;
	wire r_reset;
	wire ti_cruin;
	wire ti_extint;

	// Bidirs
	wire [0:7] tp_d;

	// Instantiate the Unit Under Test (UUT)
	tipi_top uut (
		.led0(led0), 
		.crub(crub), 
		.db_dir(db_dir), 
		.db_en(db_en), 
		.dsr_b0(dsr_b0), 
		.dsr_b1(dsr_b1), 
		.dsr_en(dsr_en), 
		.dram_a0(dram_a0), 
		.dram_en(dram_en), 
		.r_clk(r_clk), 
		.r_cd(r_cd), 
		.r_dout(r_dout), 
		.r_le(r_le), 
		.r_rt(r_rt), 
		.r_din(r_din), 
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
		crub = 4'b1110; 
		r_clk = 0;
		r_cd = 0;
		r_dout = 0;
		r_le = 0;
		r_rt = 0;
		ti_cruclk = 0;
		ti_dbin = 0;
		ti_memen = 0;
		ti_we = 0;
		ti_ph3 = 0;
		ti_a = 0;
	end
			
//		always 	
//		#10	ti_ph3 = !ti_ph3;
		
//		always 	
//		#10	ti_cruclk = !ti_cruclk;		
			
	initial begin

		// Wait 100 ns for global reset to finish, set to rest state
		#100 	
			assign ti_a = 16'h0000;
			assign ti_memen = 1;
			assign ti_we = 1;
			
		// set CRU bits
		
		#10 	
			assign ti_cruclk = 1;
			assign ti_a = 16'h1101;  // set CRU bit 0 to 0 on CRUCLK
		#10	
			assign ti_cruclk = 0;
		#10 	
			assign ti_cruclk = 1;
			assign ti_a = 16'h1103;  // set CRU bit 1 to 0 
		#10	
			assign ti_cruclk = 0;
		#10 	
			assign ti_cruclk = 1;
			assign ti_a = 16'h1105;	 // set CRU bit 2 to 0 
		#10	
			assign ti_cruclk = 0;
		#10 	
			assign ti_cruclk = 1; 	
			assign ti_a = 16'h1107;	 // set CRU bit 3 to 0 
		#10	
			assign ti_cruclk = 0;


		// read CRU bit

			assign ti_ph3 = 1; 	
		#10 	
			assign ti_a = 16'h1100;  // Read CRU bit 0 on CRU IN
		#10 
			assign ti_ph3 = 0;  // clock in read
	
	
		// read addresses 
		
			assign ti_memen = 0;
			assign ti_dbin = 1;

		#25 	
			assign ti_a = 16'h0000;   	// invald address
		#25 	  	
			assign ti_a = 16'h2000;		// DRAM address
		#25 	
			assign ti_a = 16'h3FFF;		// DRAM address
		#25 	
			assign ti_a = 16'h4000;		// DSR address

		#25 	
			assign ti_a = 16'h5FF7;		// DSR address
		#25 	
			assign ti_a = 16'h5FF9;		// CRU bit 0 address
		#25 	
			assign ti_a = 16'h5FFB;		// CRU bit 0 address
		#25 	
			assign ti_a = 16'h5FFD;		// CRU bit 0 address
		#25 	
			assign ti_a = 16'h5FFF;		// CRU bit 0 address




		#25 	
			assign ti_a = 16'h6000;
		#25 	
			assign ti_a = 16'h9FFF;
		#25 	
			assign ti_a = 16'hA000;
		#25 	
			assign ti_a = 16'hBFFF;
		#25 	
			assign ti_a = 16'hC000;
		#25 	
			assign ti_a = 16'hDFFF;
		#25 	
			assign ti_a = 16'hE000;
		#25 	
			assign ti_a = 16'hFFFF;
		
		
		
		#50
			assign ti_a = 16'hFFFF;  // idle state
			assign ti_dbin = 0;
			assign ti_memen = 1;
			assign ti_we = 1;

			
			
			
			// write states
		#25 	
			assign ti_a = 16'hFFFF;
			assign ti_dbin = 0;
			assign ti_memen = 0;
			assign ti_we = 1;
		#25 	
			assign ti_a = 16'hFFFF;
			assign ti_dbin = 0;
			assign ti_memen = 0;
			assign ti_we = 0;
		#25 	
			assign ti_a = 16'hFFFF;
			assign ti_dbin = 0;
			assign ti_memen = 0;
			assign ti_we = 1;
		#25
			assign ti_a = 16'hFFFF;  // idle state
			assign ti_dbin = 0;
			assign ti_memen = 1;
			assign ti_we = 1;
			
			

	
//		$monitor("At ",%time, dram_en, dram_a0, db_en, db_dir, led0, dsr_en, dsr_b0, dsr_b1)

	end
      
endmodule

