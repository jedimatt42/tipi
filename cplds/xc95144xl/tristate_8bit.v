`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:30:26 09/07/2017 
// Design Name: 
// Module Name:    tristate_8bit 
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
module tristate_8bit(
    input T,
    input [7:0] I,
    output [7:0] O
    );

assign O = T ? I: 8'bZ;

endmodule
