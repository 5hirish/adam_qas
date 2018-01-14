""" Package Global Constants """
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORPUS_DIR = os.path.join(os.path.dirname(__file__), 'corpus')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
SAVE_OUTPUTS = True
EXAMPLE_QUESTIONS = [
    "When was linux kernel version 4.0 released ?",
    "How to compile linux kernel ?",
    "Who is Linus Torvalds ?",
    "What's the only color Johnny Cash wears on stage ?",
    "What are the four applications bundled with Windows Vista ?",
    "How do you use a seismograph ?",
    "What is Facebook Spaces ?"]


