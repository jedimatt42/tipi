`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    23:33:22 05/22/2017 
// Design Name: 
// Module Name:    shift_pin_sout 
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
module shift_pin_sout(C, SLOAD, D, SO); 
input  C,SLOAD; 
input [7:0] D; 
output SO; 
reg [7:0] tmp; 
 
  always @(posedge C) 
  begin 
    if (SLOAD) 
      tmp = D; 
    else 
      begin 
        tmp = {tmp[6:0], 1'b0}; 
      end 
  end 
  assign SO  = tmp[7]; 
endmodule 
