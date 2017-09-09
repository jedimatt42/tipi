`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    22:07:47 09/07/2017 
// Design Name: 
// Module Name:    mux2_8bit 
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
module mux2_8bit(s, a, b, c, d, o);
input [1:0]s;
input [7:0]a;
input [7:0]b;
input [7:0]c;
input [7:0]d;
output [7:0]o;
reg [7:0]o;

always @(a or b or c or d or s)
  begin
    case (s)
      2'b00 : o = a;
      2'b01 : o = b;
      2'b10 : o = c;
      default : o = d;
    endcase
  end
endmodule