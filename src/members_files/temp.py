
from data_files import DataFile

class StringVar():
    def __init__(self, value: str) -> None:
        self._value = value

    def get(self) -> str:
        return self._value

class Parent():
    def __init__(self) -> None:
        self.data_file = DataFile()
        self.data_file.read()

        member_file = ''
        bbo_include_file = ''
        bbo_names_file = ''
        if 'member_file' in self.data_file.content:
            member_file = self.data_file.content['member_file']
        if 'bbo_include_file' in self.data_file.content:
            bbo_include_file = self.data_file.content['bbo_include_file']
        if 'bbo_names_file' in self.data_file.content:
            bbo_names_file = self.data_file.content['bbo_names_file']

        self.member_file = StringVar(value=member_file)
        self.bbo_include_file = StringVar(value=bbo_include_file)
        self.bbo_names_file = StringVar(value=bbo_names_file)
