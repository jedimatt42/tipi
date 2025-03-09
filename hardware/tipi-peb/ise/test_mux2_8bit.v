`timescale 1ns / 1ps

`include "mux2_8bit.v"

module test_mux2_8bit;

  // Inputs
  reg a_addr;
  reg [7:0] a;
  reg b_addr;
  reg [7:0] b;
  reg c_addr;
  reg [7:0] c;
  reg d_addr;
  reg [7:0] d;

  // Outputs
  wire [7:0] o;

  // Instantiate the Unit Under Test (UUT)
  mux2_8bit uut (
    .a_addr(a_addr), 
    .a(a), 
    .b_addr(b_addr), 
    .b(b), 
    .c_addr(c_addr), 
    .c(c), 
    .d_addr(d_addr), 
    .d(d), 
    .o(o)
  );

  initial begin
    // Initialize Inputs
    a_addr = 0;
    a = 8'haa;
    b_addr = 0;
    b = 8'hbb;
    c_addr = 0;
    c = 8'hcc;
    d_addr = 0;
    d = 8'hdd;

    // Wait for global reset to finish
    #1;
    
    $display("Test: no selection");
    #1 if (o != 0) begin
      $display("Error, expected o == 0, was %h", o);
      $finish;
    end
    
    $display("Test: select a");
    #1 a_addr = 1;
    #1 if (o != 8'haa) begin
      $display("Error, expected o == 8'haa, was %h", o);
      $finish;
    end
    
    $display("Test: select b");
    #1 a_addr = 0;
    #1 b_addr = 1;
    #1 if (o != 8'hbb) begin
      $display("Error, expected o == 8'hbb, was %h", o);
      $finish;
    end
    
    $display("Test: select c");
    #1 b_addr = 0;
    #1 c_addr = 1;
    #1 if (o != 8'hcc) begin
      $display("Error, expected o == 8'hcc, was %h", o);
      $finish;
    end
    
    $display("Test: select d");
    #1 c_addr = 0;
    #1 d_addr = 1;
    #1 if (o != 8'hdd) begin
      $display("Error, expected o == 8'hdd, was %h", o);
      $finish;
    end
    
    $display("Test: no selection");
    #1 d_addr = 0;
    #1 if (o != 8'h00) begin
      $display("Error, expected o == 8'h00, was %h", o);
      $finish;
    end
    
    $display("Success");    
    $finish;
  end
      
endmodule
