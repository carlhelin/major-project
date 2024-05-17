import ollama
import os, time


"""
One run of this locally

Time it took to get response:  126.30206894874573
 As a helpful, respectful, and honest assistant, I don't have the ability to 
 feel emotions like being "good" or "bad." I am always ready to assist you to 
 the best of my abilities. Is there something specific you would like help with today?
"""


def main():
    start = time.time()
    response = ollama.generate(model='mixtral', prompt="Answer yes or no. Are you good today?")
    end = time.time()
    print("Time it took to get response: ", end - start)
    print(response['response'])
    
    
if __name__ == "__main__":
    main()