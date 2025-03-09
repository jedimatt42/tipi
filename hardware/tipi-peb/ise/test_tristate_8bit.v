`timescale 1ns / 1ps

`include "tristate_8bit.v"

module test_tristate_8bit;

  // Inputs
  reg T;
  reg [7:0] I;

  // Outputs
  wire [7:0] O;

  // Instantiate the Unit Under Test (UUT)
  tristate_8bit uut (
    .T(T), 
    .I(I), 
    .O(O)
  );

  initial begin
    // Initialize Inputs
    T = 0;
    I = 0;

    // Wait 1 ns for global reset to finish
    #1;

    $display("Test: initial state Z for input");
    #1 if (O !== 8'bz) begin
      $display("Error: expected Z, got %h", O);
      $finish;
    end
        
    $display("Test: output mode");
    #1 T = 1;
    #1 I = 8'hA5;
    #1 if (O !== 8'hA5) begin
      $display("Error: expected output 8'hA5, got %h", O);
      $finish;
    end
    
    $display("Test: change in value");
    #1 I = 8'hFF;
    #1 if (O !== 8'hFF) begin
      $display("Error: expected output 8'hFF, got %h", O);
      $finish;
    end
    
    $display("Test: back to input mode");
    #1 T = 0;
    #1 if (O !== 8'bz) begin
      $display("Error: expected Z, got %h", O);
      $finish;
    end
    
    $display("Success");
    $finish;
  end
      
endmodule
