"""Compare BBO membership files."""
from dataclasses import dataclass

from members_files.csv_utils import get_dict_from_csv_file


@dataclass
class Member():
    ebu: str
    first_name: str
    last_name: str
    bbo: str
    status: str


class Compare():
    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.missing_from_include = {}
        self.missing_from_bbo = {}
        self.members_ebu = {}
        self.members_bbo = {}
        self.bbo_names = []
        self.duplicates = []
        self._compare()

    def _compare(self) -> None:
        (members, members_fields) = get_dict_from_csv_file(
            self.parent.member_file.get(), 'EBU')
        del members_fields
        for item in members.values():
            if item['EBU'] == 'EBU':
                continue
            member = Member(
                str(int(item['EBU'])),
                item['FIRSTNAME'],
                item['SURNAME'],
                item['BBOUSERNAME'].lower(),
                item['STATUS'],
            )

            self.members_ebu[member.ebu] = member

        include_list = self._get_include_list(
            self.parent.bbo_include_file.get())

        self.members_bbo = self._get_bbo_names(
            self.parent.bbo_names_file.get())

        for ebu, member in self.members_ebu.items():
            if member.bbo and member.status == 'Member':
                if member.bbo not in include_list:
                    self.missing_from_include[ebu] = self.members_ebu[ebu]
                if member.ebu not in self.members_bbo:
                    self.missing_from_bbo[ebu] = self.members_ebu[ebu]

    def _get_include_list(self, path: str) -> list:
        with open(path, 'r', encoding='utf8') as f_include:
            data = f_include.read().split('\n')
            return [name.lower() for name in data]

    def _get_bbo_names(self, path: str) -> dict:
        output = {}
        with open(path, 'r', encoding='utf8') as f_names:
            bbo_names = f_names.read().strip('\n').split('\n')

        for item in bbo_names:

            record = item.split(',')
            record = [field.strip() for field in record]
            member = Member(
                str(int(record[3])),
                record[1],
                record[2],
                record[0].lower(),
                '',
            )
            if member.ebu in output:
                self.duplicates.append(member)
                dup_member = output[member.ebu]
                self.duplicates.append(dup_member)

            output[member.ebu] = member

        if self.duplicates:
            for member in sorted(self.duplicates, key=lambda x: x.last_name):
                print(member)
            print(f'{len(bbo_names)=}')
            print(f'{len(output)=}')
        return output
