'''
Created on 1. 10. 2017

@author: patex1987

THis code demonstrates how to use the genetic algorithm to guess the unknown
word entered by the user. Here, I am using the default genetic parameters.
Try to tweak the parameters, to see how it can effect the duration of finding
the unknown word.
'''
import os
import time
import GeneticClass as gc

if __name__ == '__main__':
    UNKNOWN_TEXT = 'the pressure rises and i feel the strain'
    PEOPLE = gc.Population(UNKNOWN_TEXT)
    while PEOPLE.result_found is not True:
        PEOPLE.member_selection()
        os.system('cls')
        print(PEOPLE.summary())
        PEOPLE.combination()
        PEOPLE.mutation()
        time.sleep(0.05)
