import argparse
import json
from openai_api import OpenAIApi

USE_CACHE = True
USE_DEBUG_OUTPUT = True
PROMPT = "I'm making a metroid game. The first level is a return to Tallon 4 with Samus's ship landing and the adventure starting anew."


class AIGame:
    def __init__(self, api, skip_cache, use_gpt4):
        self.api = api
        self.system_instructions = self.load_system_instructions()
        self.skip_cache = skip_cache
        self.use_gpt4 = use_gpt4

    def load_system_instructions(self):
        with open("system_instructions.txt", 'r') as f:
            return f.read()

    def start(self):
        response_string = self.api.chat(
            self.system_instructions, PROMPT, skip_cache=self.skip_cache, use_gpt4=self.use_gpt4)
        try:
            self.process_response(response_string)
        except Exception as exc:
            print(response_string)
            raise exc

    def process_response(self, response):
        response_text = response.split("\n")
        raw_levels = response_text[:response_text.index('-')]
        rationale = response_text[response_text.index('-')+1:]
        levels = self.process_levels(raw_levels)
        if (USE_DEBUG_OUTPUT):
            self.print_debug_response(levels, rationale)
        self.print_level_diagram(levels)

    def process_levels(self, raw_levels):
        levels = dict()
        for level in raw_levels:
            split_level = level.split('\"')
            levels[split_level[1]] = {
                'name': split_level[1],
                'x': int(split_level[2][1:].split(' ')[0]),
                'y': int(split_level[2][1:].split(' ')[1]),
                'dx': int(split_level[2][1:].split(' ')[2]),
                'dy': int(split_level[2][1:].split(' ')[3])
            }
        return levels

    def print_debug_response(self, levels, rationale):
        print("RESPONSE LEVELS:")
        print(json.dumps(levels, indent=2))
        print("\nRATIONALE:")
        print('\n'.join(rationale) + '\n')

    def print_level_diagram(self, levels):
        minX, minY, maxX, maxY = 0, 0, 0, 0
        for name, data in levels.items():
            minX = min(minX, data['x'])
            minY = min(minY, data['y'])
            maxX = max(maxX, data['x'] + data['dx'])
            maxY = max(maxY, data['y'] + data['dy'])
        dimX, dimY = abs(maxX - minX), abs(maxY - minY)
        ldiag = [[' ' for _ in range(dimX)] for _ in range(dimY)]
        for name, data in levels.items():
            lx, ly, ldx, ldy = data['x'], data['y'], data['dx'], data['dy']
            namechar = name[0]
            coords = []
            for i in range(ldx):
                for j in range(ldy):
                    coords.append((lx + i, ly + j))
            for tx, ty in coords:
                ldiag[ty][tx] = namechar
        print('\n')
        for row in ldiag:
            print(''.join(row))
        print('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip_cache', action='store_true',
                        help='Skip the cache and call OpenAI api')
    parser.add_argument('--use_gpt4', action='store_true',
                        help='Enable GPT-4 usage')
    args = parser.parse_args()

    api_obj = OpenAIApi()
    game = AIGame(api_obj, args.skip_cache, args.use_gpt4)
    game.start()
