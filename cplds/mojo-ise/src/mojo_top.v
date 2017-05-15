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

reg [0:7] dsr_data_rom [0:8191];

integer i;
initial begin
  $readmemh("../../../dsr/tipi.hex", dsr_data_rom);
end

reg [0:7] dsr_q;
wire a15;

wire rst = ~rst_n; // make reset active high

wire tipi_data_out;
wire tipi_control_out;
wire tipi_dsr_out;

// a CRU bit to act as device-enable
reg crubit_q;
reg crupireset_q;

// latched data channel
reg [7:0] data_q;
// latched control channel
reg [7:0] control_q;

// shift register signals from RPi
reg [7:0] rdata_q;
reg [7:0] rdata_latch;
reg [7:0] rcontrol_q;
reg [7:0] rcontrol_latch;
reg [7:0] dbus_q; // internal register so we can choose which other register goes to data output bus.

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

// need to consider crubit_q also... 
assign tipi_data_out = (crubit_q && ~ti_memen && ti_dbin && ti_a == 16'h5ffb) ? 1'b0 : 1'b1;
assign tipi_control_out = (crubit_q && ~ti_memen && ti_dbin && ti_a == 16'h5ff9) ? 1'b0 : 1'b1;
assign tipi_dsr_out = (crubit_q && ~ti_memen && ti_dbin && ti_a >= 16'h4000 && ti_a < 16'h5ff8) ? 1'b0 : 1'b1;

always @(negedge ti_we) begin
  if (crubit_q && ~ti_memen && ti_a == 16'h5fff) begin
    data_q <= ti_data;
  end
end

always @(negedge ti_we) begin
  if (crubit_q && ~ti_memen && ti_a == 16'h5ffd) begin
    control_q <= ti_data;
  end
end

always @(negedge ti_cruclk) begin
  if (ti_a[4:7] == cru_base && ti_a[0:3] == 4'b0001) begin
    if (ti_a[8:14] == 7'h00) begin
	   crubit_q <= ti_a[15];
	 end
    if (ti_a[8:14] == 7'h01) begin
	   crupireset_q <= ti_a[15];
	 end
  end
end

integer rom_idx;

// Use block ram, for the DSR ROM. Requires the clock for input.
always @(posedge clk) begin
  rom_idx <= ti_a[3:15];
  dsr_q <= dsr_data_rom[rom_idx];
end

always @(posedge rpi_cclk) begin
  if (rpi_le) rcontrol_latch <= rcontrol_q;
  else rcontrol_q <= { rcontrol_q[6:0], rpi_sdata };
end

always @(posedge rpi_dclk) begin
  if (rpi_le) rdata_latch <= rdata_q;
  else rdata_q <= { rdata_q[6:0], rpi_sdata };
end

always @(posedge clk) begin
  if (ti_a[3:15] == 13'h1ff9) dbus_q <= rcontrol_q;
  else if (ti_a[3:15] == 13'h1ffb) dbus_q <= rdata_q;
  else if (ti_a[3:15] >= 13'h0000 && ti_a[3:15] < 13'h1ff9) dbus_q <= dsr_q;
  else dbus_q <= 8'h00;
end

assign dsr_d = dbus_q;
assign tipi_dbus_oe = (crubit_q && ~ti_memen && ti_dbin && ti_a >= 16'h4000 && ti_a < 16'h5ffd) ? 1'b0 : 1'b1;

assign rpi_d = data_q;
assign rpi_s = control_q;

assign rpi_reset = !crupireset_q;

assign led[0] = crubit_q;
assign led[1] = !crupireset_q;
assign led[3:2] = control_q[1:0];
assign led[7:4] = rcontrol_q[3:0];

endmodule
