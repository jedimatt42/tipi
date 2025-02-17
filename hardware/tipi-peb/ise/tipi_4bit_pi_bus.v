`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    01:54:59 02/17/2025 
// Design Name: 
// Module Name:    tipi_4bit_pi_bus
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

module tipi_4bit_pi_bus (
    input wire clk,            // Clock from MCU
    input wire reset,          // Reset signal from MCU
    inout wire [3:0] data,     // 4-bit bidirectional data bus
    input wire [7:0] TD,       // Exposed TD register (Read by MCU)
    input wire [7:0] TC,       // Exposed TC register (Read by MCU)
    output reg [7:0] RD,       // Exposed RD register (Written by MCU)
    output reg [7:0] RC        // Exposed RC register (Written by MCU)
);

    reg [7:0] shift_reg;       // Temporary shift register for transfers
    reg [1:0] bit_count;       // Tracks the number of 4-bit transfers
    reg [1:0] sel;             // Internalized register selection
    reg rw;                    // Internalized read/write control

    wire is_output = (rw == 1'b1); // Only output data if in read mode

    // Output correct 4-bit chunk based on bit_count
    assign data = (is_output) ? (bit_count[0] ? shift_reg[3:0] : shift_reg[7:4]) : 4'bz;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            shift_reg <= 8'h00;
            bit_count <= 2'b00;
            sel <= 2'b00;   // Clear selection register
            rw <= 1'b1;     // Default to read mode
        end else begin
            if (bit_count == 2'b00) begin
                // First clock: Capture 'sel' from lower 2 bits of the data bus
                sel <= data[1:0];

                // Determine read or write mode based on the selected register
                case (data[1:0])
                    2'b00: begin shift_reg <= TD; rw <= 1'b1; end // TD → Read
                    2'b01: begin shift_reg <= TC; rw <= 1'b1; end // TC → Read
                    2'b10: begin rw <= 1'b0; end // RD → Write
                    2'b11: begin rw <= 1'b0; end // RC → Write
                endcase
            end else begin
                if (rw) begin
                    // Read operation: shift out next 4 bits
                    shift_reg <= {shift_reg[3:0], 4'b0000};
                end else begin
                    // Write operation: shift in new 4 bits
                    shift_reg <= {shift_reg[3:0], data};
                    if (bit_count == 2'b01) begin
                        // After receiving full 8 bits, store data into correct register
                        case (sel)
                            2'b10: RD <= {shift_reg[3:0], data};
                            2'b11: RC <= {shift_reg[3:0], data};
                        endcase
                    end
                end
            end
            bit_count <= bit_count + 1;
        end
    end
endmodule

