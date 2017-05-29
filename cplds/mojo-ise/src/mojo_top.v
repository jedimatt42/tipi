`include "crubits.v"
`include "latch_8bit.v"
`include "shift_pload_sout.v"
`include "shift_sin_pout.v"
`include "rom.v"
module mojo_top(
    // 50MHz clock input
    input clk,
    // Input from reset button (active low)
    input rst_n,
    // cclk input from AVR, high when AVR is ready
    input cclk,
    // Outputs to the 8 onboard LEDs
    output[7:0]led,
    // AVR SPI connections
    output spi_miso,
    input spi_ss,
    input spi_mosi,
    input spi_sck,
    // AVR ADC channel select
    output [3:0] spi_channel,
    // Serial connections
    input avr_tx, // AVR Tx => FPGA Rx
    output avr_rx, // AVR Rx => FPGA Tx
    input avr_rx_busy, // AVR Rx buffer full

    // -------- i/o to TI-99/4A -------------
     
    // TI address bus. bit 0 is MSB per TI numbering.
    input [0:15]ti_a,
    // TI data bus inputs. bit 0 is MSB.
    input [0:7]ti_data,
    // TI Memory enable (active low)
    input ti_memen,
    // TI Write enable (active low)
    input ti_we,
    // Device CRU base address nibble 'n' in 0x1n00
    input [3:0]cru_base,
    // TI Memory Read (active high)
    input ti_dbin,
    // TI CRU Clock (active low)
    input ti_cruclk,
    
    // DSR ROM Data output from 0x4000 to 0x5ff8, or RPi registers at 0x5ff9 & 0x5ffb
    output [0:7]dsr_d,
    // Control OE* on a bus transmitter to allow DSR ROM or RPi registers on TI data bus.
    output tipi_dbus_oe,

	 // -------- input from Raspberry Pi ---------

    // RPi shift register clock
    input rpi_sclk,
	 // RPi register selection
	 input [1:0]rpi_regsel,
	 // RPi data in to register
    input rpi_sdata_out,	 
    // RPi register latch
	 input rpi_sle,
 
	 // RPi data output from register
	 output rpi_sdata_in,
    // control reset of RPi service scripts
    output rpi_reset
);

// Mojo Dev Board Noise
wire rst = ~rst_n; // make reset active high
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

// TI CRU state
wire [0:3]cru_state;
crubits cru(cru_base, ti_cruclk, ti_a[0:14], ti_a[15], cru_state);
wire cru_dsr_en = cru_state[0];

// Raspberry PI reset trigger on cru, second bit.
assign rpi_reset = ~cru_state[1];


////// From RPi -> TI-99/4A

// RD serial in parallel output latch
wire tipi_rd_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a == 16'h5ffb);
wire rd_cs = (rpi_regsel == 2'b00);
wire [0:7]ti_dbus_rd;
shift_sin_pout shift_rd(rpi_sclk, rd_cs, rpi_sle, rpi_sdata_out, ti_dbus_rd);

// RC serial in parallel output latch
wire tipi_rc_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a == 16'h5ff9);
wire rc_cs = (rpi_regsel == 2'b01);
wire [0:7]ti_dbus_rc;
shift_sin_pout shift_rc(rpi_sclk, rc_cs, rpi_sle, rpi_sdata_out, ti_dbus_rc);

// TIPI DSR
wire tipi_dsr_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a >= 16'h4000 && ti_a < 16'h5ff8);
wire [0:7]ti_dbus_dsr;
rom dsr(clk, tipi_dsr_out, ti_a[3:15], ti_dbus_dsr);

////// Wiring up the TI data bus

// Invert OE for bus driver chip
assign tipi_dbus_oe = ~(tipi_dsr_out || tipi_rc_out || tipi_rd_out);
reg [0:7]dbus_out;
// TODO, merge ti_data and dsr_d as single 8 bit bi-directional bus
always @(tipi_dsr_out or tipi_rc_out or tipi_rd_out) begin
    if (tipi_dsr_out) dbus_out = ti_dbus_dsr;
	 else if (tipi_rc_out) dbus_out = ti_dbus_rc;
	 else if (tipi_rd_out) dbus_out = ti_dbus_rd;
	 else dbus_out = 8'bzzzzzzzz;
end

assign dsr_d = dbus_out;

////// From TI-99/4A to RPi

// TD output latch
wire tipi_td_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5fff);
wire [0:7]rpi_td;
latch_8bit td(tipi_td_le, ti_data, rpi_td);

// shift register out to RPi for TD
wire td_clk = rpi_sclk && (rpi_regsel == 2'b10);
wire td_out;
wire [7:0]debug_td_out;
shift_pload_sout shift_td(td_clk, rpi_sle, rpi_td, td_out, debug_td_out);

// TC output latch
wire tipi_tc_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5ffd);
wire [0:7]rpi_tc;
latch_8bit tc(tipi_tc_le, ti_data, rpi_tc);

// shift register out to RPi for TC
wire tc_clk = rpi_sclk && (rpi_regsel == 2'b11);
wire tc_out;
wire [7:0]debug_tc_out;
shift_pload_sout shift_tc(tc_clk, rpi_sle, rpi_tc, tc_out, debug_tc_out);

assign rpi_sdata_in = (rpi_regsel == 2'b11) ? tc_out : td_out;

// Debugging LEDs
assign led[7:0] = { tc_clk, tc_out, rpi_sclk, rpi_sle, debug_tc_out[7:4] };

endmodule
