`ifndef _rom_vh_
`define _rom_vh_

// The ROM, responsible for being an 8k rom with preloaded data.
module rom(
    // FPGA primary clock input
    input clk,
    // address bus.
    input [0:12]addr,
    // DSR ROM Data output
    output [0:7]data
);

reg [0:7] rom_data [0:8191];

initial begin
  $readmemh("../../../dsr/tipi.hex", rom_data);
end

reg [0:7] data_q;

// Use block ram, for the DSR ROM. Requires the clock for input.
always @(posedge clk) begin
  data_q <= rom_data[addr];
end

assign data = data_q;

endmodule

`endif 
