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
    reg busdir;                // Internalized read/write control 0 input, 1 output

    // Output correct 4-bit chunk based on bit_count
    assign data = (busdir == 1'b1) ? shift_reg[7:4] : 4'bz;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            shift_reg <= 8'h00;
            bit_count <= 2'b00;
            sel <= 2'b00;   // Clear selection register
            busdir <= 1'b0;     // Default to input on bus
        end else begin
            if (bit_count == 2'b00) begin
                // First clock: Capture 'sel' from lower 2 bits of the data bus
                sel <= data[1:0];
                case (data[1:0])
                    // Second clock: Load shift_reg with the selected register's value
                    2'b00: begin shift_reg <= TD; busdir <= 1'b1; end // TD → output
                    2'b01: begin shift_reg <= TC; busdir <= 1'b1; end // TC → output
                    2'b10: begin busdir <= 1'b0; end // RD → input
                    2'b11: begin busdir <= 1'b0; end // RC → input
                endcase         
            end else if (bit_count == 2'b01) begin
                if (busdir) begin
                    // Read operation: shift out high nibble
                    shift_reg <= {shift_reg[3:0], 4'b0000};
                end else begin
                    // Write operation: shift in high nibble
                    shift_reg <= {shift_reg[3:0], data};
                end
            end else if (bit_count == 2'b10) begin
                if (busdir) begin
                    // Read operation: shift out low nibble
                    shift_reg <= {shift_reg[3:0], 4'b0000};
                end else begin
                    // Write operation: shift in low nibble
                    shift_reg <= {shift_reg[3:0], data};
                    // After receiving full 8 bits, store data into correct register
                    case (sel)
                        2'b10: RD <= {shift_reg[3:0], data};
                        2'b11: RC <= {shift_reg[3:0], data};
                    endcase
                end
            end
            bit_count <= bit_count + 1;
        end
    end
endmodule

