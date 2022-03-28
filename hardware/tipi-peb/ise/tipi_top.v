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
`include "rpi_reg_select.v"
`include "shift_pload_nib_out.v"
`include "shift_nib_in_pout.v"
`include "tristate_8bit.v"
`include "mux2_8bit.v"

module tipi_top(
		output led0,
		
		input[0:3] crub,
		
		output db_dir,
		output db_en,
		output dsr_b0,
		output dsr_b1,
		output dsr_en,
		
		input r_clk,
		input r_le,
		inout [0:3] r_nib,
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
wire cru_dev_en = cru_state[0];
assign ti_cruin = cru_regout;
assign r_reset = ~cru_state[1];
// For a 32k 27C256 chip, these control bank switching.
assign dsr_b0 = cru_state[2];
assign dsr_b1 = cru_state[3];
// For a 8k 27C64 chip, these need to stay constant
// assign dsr_b0 = 1'bz; // not connected on 27C64
// assign dsr_b1 = 1'b1; // Active LOW is PGM on 27C64

// Latches && Shift Registers for TI to RPi communication - TC & TD
wire [3:0]reg_sel;
rpi_reg_select select_nibble(r_reset, r_clk, r_nib, reg_sel);

// Register selection:
//   first nibble of 3 nibble sequence selects register.
// The following aliases should help.
wire tipi_rc = reg_sel[0];
wire tipi_rd = reg_sel[1];
wire tipi_tc = reg_sel[2];
wire tipi_td = reg_sel[3];

// address comparisons
wire rc_addr = ti_a == 16'h5ff9;
wire rd_addr = ti_a == 16'h5ffb;
wire tc_addr = ti_a == 16'h5ffd;
wire td_addr = ti_a == 16'h5fff;

// TD Latch - TI writable byte for data output
wire tipi_td_le = (cru_dev_en && ~ti_we && ~ti_memen && td_addr);
wire [0:7]rpi_td;
latch_8bit td(tipi_td_le, tp_d, rpi_td);

// TC Latch - TI writable byte for protocol control
wire tipi_tc_le = (cru_dev_en && ~ti_we && ~ti_memen && tc_addr);
wire [0:7]rpi_tc;
latch_8bit tc(tipi_tc_le, tp_d, rpi_tc);

// TD Shift output - Raspberry PI readable TI Data byte
wire [3:0]td_out;
shift_pload_nib_out shift_td(r_clk, tipi_td, r_le, rpi_td, td_out);

// TC Shift output - Raspberry PI readable TI Control byte
wire [3:0]tc_out;
shift_pload_nib_out shift_tc(r_clk, tipi_tc, r_le, rpi_tc, tc_out);


// Data from the RPi, to be read by the TI.

// RD
wire [0:7]tipi_db_rd;
shift_nib_in_pout shift_rd(r_clk, tipi_rd, r_le, r_nib, tipi_db_rd);

// RC
wire [0:7]tipi_db_rc;
shift_nib_in_pout shift_rc(r_clk, tipi_rc, r_le, r_nib, tipi_db_rc);

// RPI r_nib nibble transfer mux

// r_nib as input -> reg_sel_in, rc_in, rd_in. 
// r_nib needs to output either tc_out or td_out based on 
//  tipi_tc or tipi_td;
assign r_nib = tipi_tc ? tc_out : (tipi_td ? td_out : 4'bz);

//-- Databus control
wire tipi_read = cru_dev_en && ~ti_memen && ti_dbin;
wire tipi_dsr_en = tipi_read && ti_a >= 16'h4000 && ti_a < 16'h5ff8;

// drive the dsr eprom oe and cs lines.
assign dsr_en = ~(tipi_dsr_en);
// drive the 74hct245 oe and dir lines.
assign db_en = ~(cru_dev_en && ti_a >= 16'h4000 && ti_a < 16'h6000);
assign db_dir = tipi_read;

// register to databus output selection
wire [0:7]rreg_mux_out; 
mux2_8bit rreg_mux(rc_addr, tipi_db_rc, rd_addr, tipi_db_rd, tc_addr, rpi_tc, td_addr, rpi_td, rreg_mux_out);

wire [0:7]tp_d_buf;
wire dbus_ts_en = cru_state[0] && ~ti_memen && ti_dbin && ( ti_a >= 16'h5ff8 && ti_a < 16'h6000 );
tristate_8bit dbus_ts(dbus_ts_en, rreg_mux_out, tp_d_buf);

assign tp_d = tp_d_buf;


assign led0 = cru_state[0] && db_en;


endmodule
