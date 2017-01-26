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
	 
	 input tipi_data_out,
	 input tipi_control_out,
	 input tipi_dsr_out,
	 
	 input [0:15]ti_a,
	 input [7:0]ti_data,
	 input ti_memen,
	 input ti_we,
	 input [3:0]cru_base,
	 input ti_dbin,
	 input ti_cruclk,
	 input ti_reset
    );

wire rst = ~rst_n; // make reset active high
reg [7:0] data_q;
reg [7:0] control_q;

// these signals should be high-z when not used
assign spi_miso = 1'bz;
assign avr_rx = 1'bz;
assign spi_channel = 4'bzzzz;

assign tipi_data_out = 1'b1;
assign tipi_control_out = 1'b1;
assign tipi_dsr_out = 1'b1;

always @(negedge ti_we) begin
  if (~ti_memen && ti_a == 16'h5fff) begin
    data_q <= ti_data;
  end
  if (~ti_memen && ti_a == 16'h5ffd) begin
    control_q <= ti_data;
  end
end



assign led[7:4] = data_q[7:4];
assign led[3:0] = control_q[3:0];

endmodule