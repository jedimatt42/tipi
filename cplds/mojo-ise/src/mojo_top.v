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
     
    // Control OE* on a bus transmitter to allow RPi data on TI data bus.
    output tipi_data_out,
    // Control OE* on a bus transmitter to allow RPi control signals on TI data bus.
    output tipi_control_out,
    // Control OE* on a bus transmitter to allow DSR ROM on TI data bus.
    output tipi_dsr_out,
     
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
    // TI Reset (active low)
    input ti_reset,
    
    // Data output to RPi latched from 0x5fff
    output [7:0]rpi_d,
    // Control signal output to RPi latched from 0x5ffd
    output [7:0]rpi_s,
	 // DSR ROM Data output from 0x4000 to 0x5ff8
	 output [0:7]dsr_d
);

reg [0:7] dsr_data_rom [0:8191];
initial begin 
  $readmemh("../../../dsr/tipi.hex", dsr_data_rom);
end

reg [0:7] dsr_q;
wire a15;

wire rst = ~rst_n; // make reset active high
wire dsr_oe;

// a CRU bit to act as device-enable
reg crubit_q;

// latched data channel
reg [7:0] data_q;
// latched control channel
reg [7:0] control_q;

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;
assign a15 = ti_a[15];

// need to consider crubit_q also... 
assign tipi_data_out = (crubit_q && ~ti_memen && ti_dbin && ti_a == 16'h5ffb) ? 1'b0 : 1'b1;
assign tipi_control_out = (crubit_q && ~ti_memen && ti_dbin && ti_a == 16'h5ff9) ? 1'b0 : 1'b1;
assign dsr_oe = (crubit_q && ~ti_memen && ti_dbin && ti_a > 16'h3fff && ti_a < 16'h5ff8) ? 1'b0 : 1'b1;
assign tipi_dsr_out = dsr_oe;

always @(negedge ti_we) begin
  if (crubit_q && ~ti_memen) begin
    if (ti_a == 16'h5fff) begin
      data_q <= ti_data;
    end else 
    if (ti_a == 16'h5ffd) begin
      control_q <= ti_data;
    end
  end
end

always @(negedge ti_cruclk) begin
  if (ti_a[0:3] == 4'b0001 && (ti_a[4:7] == cru_base && ti_a[8:14] == 7'h00)) begin
    crubit_q <= ti_a[15];
  end
end

always @(a15) begin
  dsr_q = dsr_data_rom[ti_a[3:15]];
end

assign dsr_d = dsr_q;

assign rpi_d = data_q;
assign rpi_s = control_q;

assign led[7:1] = control_q[6:0];
assign led[0] = crubit_q;

endmodule
