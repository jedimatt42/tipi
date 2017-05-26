`include "crubits.v"
`include "latch_8bit.v"
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

    // --------------------------------------------------
     
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
    
    // Inputs for data and control registers from RPi
    input rpi_cclk,
    input rpi_dclk,
    input rpi_sdata,
    input rpi_le,
	 
    // Data output to RPi latched from 0x5fff
    output [7:0]rpi_d,
    // Control signal output to RPi latched from 0x5ffd
    output [7:0]rpi_s,
    // DSR ROM Data output from 0x4000 to 0x5ff8, or RPi registers at 0x5ff9 & 0x5ffb
    output [0:7]dsr_d,
    // Control OE* on a bus transmitter to allow DSR ROM or RPi registers on TI data bus.
    output tipi_dbus_oe,
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

// ignore for now... not controling tristate buffers at this time
wire tipi_data_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a == 16'h5ffb) ? 1'b0 : 1'b1;
wire tipi_control_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a == 16'h5ff9) ? 1'b0 : 1'b1;

// TD output latch
// -- address and write operation decoding
wire tipi_td_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5fff);
wire [0:7] rpi_td;
latch_8bit td(tipi_td_le, ti_data, rpi_td);

// TC output latch
// -- address and write operation decoding
wire tipi_tc_le = (cru_dsr_en && ~ti_we && ~ti_memen && ti_a == 16'h5ffd);
wire [0:7] rpi_tc;
latch_8bit tc(tipi_tc_le, ti_data, rpi_tc);

// TIPI DSR
wire tipi_dsr_out = (cru_dsr_en && ~ti_memen && ti_dbin && ti_a >= 16'h4000 && ti_a < 16'h5ff8);
rom dsr(clk, tipi_dsr_out, ti_a[3:15], dsr_d);

// Invert OE for bus driver chip
assign tipi_dbus_oe = ~tipi_dsr_out;
assign led[7:0] = { cru_state[0:1], rpi_td[5:7], rpi_tc[5:7] };

// high-z or static value for unused output signals
assign rpi_s = 8'bzzzzzzzz;
assign rpi_d = 8'bzzzzzzzz;

endmodule
