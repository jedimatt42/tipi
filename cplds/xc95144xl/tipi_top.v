`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    13:20:25 07/15/2017 
// Design Name: 
// Module Name:    tipi_top 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
`include "crubits.v"
`include "latch_8bit.v"
`include "shift_pload_sout.v"
`include "shift_sin_pout.v"
module tipi_top(
		output led0,
		
		input[0:3] crub,
		
		output db_dir,
		output db_en,
		output dsr_b0,
		output dsr_b1,
		output dsr_en,
		
		input r_clk,
		// 0 = Data or 1 = Control byte selection
		input r_dc,
		input r_dout,
		input r_le,
		// R|T 0 = RPi or 1 = TI originating data 
		input r_rt,
		output r_din,
		output r_reset,

		input ti_cruclk,
		input ti_dbin,
		input ti_memen,
		input ti_we,
		input ti_ph3,
		output ti_cruin,
		output ti_extint,
		
		input[0:15] ti_a,
		inout[0:7] tp_d
		
    );

// Unused
assign ti_extint = 1'bz; // try to avoid triggering this interrupt ( temporarily an input )

// Process CRU bits
wire ti_cruout = ti_a[15];
wire [0:3]cru_state;
wire cru_regout;
crubits cru(~crub, ti_cruclk, ti_memen, ti_ph3, ti_a[0:14], ti_cruout, cru_regout, cru_state);
wire cru_dsr_en = cru_state[0];
assign ti_cruin = cru_regout;
assign r_reset = cru_state[1];
// For a 32k 27C256 chip, these control bank switching.
// assign dsr_b0 = cru_state[2];
// assign dsr_b1 = cru_state[3];
// For a 8k 27C64 chip, these need to stay constant
assign dsr_b0 = 1'bz; // not connected on 27C64
assign dsr_b1 = 1'b1; // Active LOW is PGM on 27C64

// Latches && Shift Registers for TI to RPi communication - TC & TD

// Register selection:
// r_rt and r_dc combine to select the rd rc td and tc registers. 
// we will assert that r_rt == 0 is RPi output register
//                     r_rt == 1 is TI output register
//                     r_dc == 0 is data register
//                     r_dc == 1 is control register
// The following aliases should help.
wire tipi_rd = ~r_rt && ~r_dc;
wire tipi_rc = ~r_rt && r_dc;
wire tipi_td = r_rt && ~r_dc;
wire tipi_tc = r_rt && r_dc; 

// TD Latch
wire tipi_td_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5fff);
wire [0:7]rpi_td;
latch_8bit td(tipi_td_le, tp_d, rpi_td);

// TC Latch
wire tipi_tc_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5ffd);
wire [0:7]rpi_tc;
latch_8bit tc(tipi_tc_le, tp_d, rpi_tc);

// TD Shift output
wire td_clk = r_clk && tipi_td;
wire td_out;
shift_pload_sout shift_td(td_clk, r_le, rpi_td, td_out);

// TC Shift output
wire tc_clk = r_clk && tipi_tc;
wire tc_out;
shift_pload_sout shift_tc(tc_clk, r_le, rpi_tc, tc_out);

// Select if output is from the data or control register
assign r_din = r_dc ? td_out : tc_out;

// Data from the RPi, to be read by the TI.

// RD
wire rrd_clk = r_clk && tipi_rd;
wire [0:7]tipi_db_rd;
shift_sin_pout shift_rd(rrd_clk, r_le, r_dout, tipi_db_rd);

// RC
wire rrc_clk = r_clk && tipi_rc;
wire [0:7]tipi_db_rc;
shift_sin_pout shift_rc(rrc_clk, r_le, r_dout, tipi_db_rc);

//-- Databus control

wire tipi_read = cru_dsr_en && ~ti_memen && ti_dbin;
wire tipi_dsr_en = tipi_read && ti_a >= 16'h4000 && ti_a < 16'h5ff8;

wire tipi_rd_en = tipi_read && ti_a == 16'h5ffb;
wire tipi_rc_en = tipi_read && ti_a == 16'h5ff9;

// Currently hacked up to just read the td register, maybe
reg [0:7]dbus_out;
always @(*) begin
    if (tipi_read && ti_a == 16'h5fff) dbus_out = rpi_td;
    else dbus_out = 8'bzzzzzzzz;
end
assign tp_d = dbus_out;

// drive the dsr eprom oe and cs lines.
assign dsr_en = ~(tipi_dsr_en);
// drive the 74hct245 oe and dir lines.
assign db_en = ~(cru_state[0] && ti_a >= 16'h4000 && ti_a < 16'h6000);
assign db_dir = tipi_read;

assign led0 = cru_state[0] && db_en;

endmodule
