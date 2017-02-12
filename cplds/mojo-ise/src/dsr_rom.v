`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:03:24 02/11/2017 
// Design Name: 
// Module Name:    dsr_rom 
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
module dsr_rom(
    input [12:0] addr,
    output [0:7] data
    );
	 
reg [7:0] data_ROM [0:27];

integer i;
initial begin
  $readmemh("../../../dsr/tipi.hex", data_ROM);
  for (i=0; i<28; i=i+1)
    $display("%d:%h", i, data_ROM[i]);
end

assign data = data_ROM[addr];

endmodule
