import sbsv

def parse_meta(file: str) -> sbsv.parser:
    parser = sbsv.parser()
    parser.add_schema("[meta] [type: str] [origin: str] [name: str]")
    with open(file, 'r') as f:
        parser.load(f)        
    return parser


if __name__ == '__main__':
    result = parse_meta('meta.sbsv')
    print(result)