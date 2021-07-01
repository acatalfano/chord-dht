class Server:
    '''
    a server node in the DHT
    '''

    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name
