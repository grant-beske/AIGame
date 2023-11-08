from openai_api import OpenAIApi

USE_CACHE = True
USE_DEBUG_OUTPUT = True
PROMPT = "I'm making a metroid game. The first level is a return to Tallon 4 with Samus's ship landing and the adventure starting anew."

class AIGame:
    def __init__(self, api):
        self.api = api
        self.system_instructions = self.load_system_instructions()

    def load_system_instructions(self):
        with open("system_instructions.txt", 'r') as f:
            return f.read()

    def start(self):
        response_string = self.api.chat(self.system_instructions, PROMPT, use_cache=USE_CACHE)
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
        if (USE_DEBUG_OUTPUT): self.print_debug_response(rationale, levels)
        self.print_level_diagram(levels)
        
    def process_levels(self, raw_levels):
        return {level.split('\'')[1]: {
                    'name': level.split('\'')[1],
                    'x': int(level.split('\'')[2][1:].split(' ')[0]), 
                    'y': int(level.split('\'')[2][1:].split(' ')[1]),
                    'dx': int(level.split('\'')[2][1:].split(' ')[2]),
                    'dy': int(level.split('\'')[2][1:].split(' ')[3])
                } for level in raw_levels
            }

    def print_debug_response(self, levels, rationale):
        print("RESPONSE LEVELS:")
        print(levels)
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
    api_obj = OpenAIApi()
    game = AIGame(api_obj)
    game.start()
    