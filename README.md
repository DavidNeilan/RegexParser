# Python Regex Parser
This "Regex Parser" was written as part of my 2019 Graph Theory module. 

## Basic Usage:

* Input:`python parser.py "a?" "a"`\
  Expected Output:`True`
  
* Input:`python parser.py "a.(b|d).c*" "abdc"`\
  Expected Output:`False`
  
* Input:`python parser.py "(a|b)*" "abbaa"`\
  Expected Output:`True`

## Features

* Python type hinting is employed throughout
* Code is well documented and follows good practise
* A small test expressions can be found in the file

## Notes:
My initial infix -> postfix convert was based on work I first saw on http://condor.depaul.edu/ichu/csc415/notes/notes9/Infix.htm \
I found the instructions outlined here helpful however I was unable to properly implement grouping until it was better
covered in detail during a video lecture by our class instructor.

My initial approach to evaluating an expression was to employ a functional approach whereby the the regex expression
would evaluated one token at a time and each operator would call a function. Each function would have a copy of the 
state of the current output and would from a tree-like structure that could be used to evaluated to match the regex.
(Some examples of my function approach can be seen in early commits)

I did not get functional approach to work and when we covered Thompson Construction in class I quickly switched approach
using it instead. I followed a video lecture also conducted by our instructor and modified it along with guidance
form http://www.oxfordmathcenter.com/drupal7/node/628 to build my parser. 