from openai_api import OpenAIApi

USE_CACHE = True

with open("system_instructions.txt", 'r') as f:
    system_instructions = f.read()
prompt = "I'm making a metroid game. The first level is a return to Tallon 4 with Samus's ship landing and the adventure starting anew."

api_obj = OpenAIApi()
response_string = api_obj.chat(system_instructions, prompt, use_cache=USE_CACHE)

try:
    response_text = response_string.split("\n")
    response_levels = response_text[:response_text.index('-')]
    response_rationale = response_text[response_text.index('-')+1:]

    print("RESPONSE LEVELS:")
    for line in response_levels:
        print(line)

    print("\nRATIONALE:")
    print('\n'.join(response_rationale) + '\n')

    level = response_levels[0]
    levels = {level.split('\'')[1]: {'name': level.split('\'')[1],
                                     'x': int(level.split('\'')[2][1:].split(' ')[0]), 
                                     'y': int(level.split('\'')[2][1:].split(' ')[1]),
                                     'dx': int(level.split('\'')[2][1:].split(' ')[2]),
                                     'dy': int(level.split('\'')[2][1:].split(' ')[3])} for level in response_levels}
    print(levels)

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


except Exception as exc:
    print(exc)
    print(response_string)
    exit(0)
