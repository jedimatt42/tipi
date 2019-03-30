#!/usr/bin/python

import sys, time
import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

def setpin(pin, state):
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, state)

def red(state):
  setpin(redPin, state)
  setpin(greenPin, GPIO.LOW)
  setpin(bluePin, GPIO.LOW)

def green(state):
  setpin(redPin, GPIO.LOW)
  setpin(greenPin, state)
  setpin(bluePin, GPIO.LOW)

def blue(state):
  setpin(redPin, GPIO.LOW)
  setpin(greenPin, GPIO.LOW)

def yellow(state):
  setpin(redPin, state)
  setpin(greenPin, state)
  setpin(bluePin, GPIO.LOW)

def cyan(state):
  setpin(redPin, GPIO.LOW)
  setpin(greenPin, state)
  setpin(bluePin, state)

def magenta(state):
  setpin(redPin, state)
  setpin(greenPin, GPIO.LOW)
  setpin(bluePin, state)

def white(state):
  setpin(redPin, state)
  setpin(greenPin, state)
  setpin(bluePin, state)

GPIO.setwarnings(False)

try:
  while True:
    time.sleep(0.9)
    green(GPIO.HIGH)
    time.sleep(0.1)
    green(GPIO.LOW)
except: 
  white(GPIO.LOW)

